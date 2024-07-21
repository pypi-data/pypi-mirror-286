from __future__ import annotations

import importlib
import importlib.util
import linecache
import os
import sys
import traceback
from contextvars import ContextVar
from pathlib import Path
from types import TracebackType
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

from chalk._lsp.error_builder import DiagnosticBuilder, LSPErrorBuilder
from chalk.features import Feature, FeatureSetBase, unwrap_feature
from chalk.features.feature_field import WindowConfigResolved
from chalk.features.resolver import RESOLVER_REGISTRY, Resolver
from chalk.features.underscore import UnderscoreAttr, UnderscoreCall, UnderscoreItem, UnderscoreRoot
from chalk.gitignore.gitignore_parser import parse_gitignore
from chalk.gitignore.helper import IgnoreConfig, get_default_combined_ignore_config, is_ignored
from chalk.parsed.duplicate_input_gql import (
    DiagnosticSeverityGQL,
    FailedImport,
    PositionGQL,
    PublishDiagnosticsParams,
    RangeGQL,
)
from chalk.sql._internal.sql_file_resolver import get_sql_file_resolvers, get_sql_file_resolvers_from_paths
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.streams import get_duration_secs
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.paths import get_directory_root, search_recursively_for_file

_logger = get_logger(__name__)


def _py_path_to_module(path: Path, repo_root: Path) -> str:
    try:
        p = path.relative_to(repo_root)
    except ValueError:
        p = path
    ans = str(p)[: -len(".py")].replace(os.path.join(".", ""), "").replace(os.path.sep, ".")
    if ans.endswith(".__init__"):
        # Do not import __init__.py directly. Instead, import the module
        ans = ans[: -len(".__init__")]
    return ans


has_imported_all_files = False


def import_all_files_once(
    file_allowlist: Optional[List[str]] = None,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
    override: bool = False,
) -> List[FailedImport]:
    global has_imported_all_files
    if has_imported_all_files:
        return []
    failed = import_all_files(
        file_allowlist=file_allowlist, project_root=project_root, only_sql_files=only_sql_files, override=override
    )
    has_imported_all_files = True
    return failed


supported_aggs = ("sum", "count", "mean", "std", "var", "min", "max")


def parse_windowed_materialization(f: Feature) -> Tuple[WindowConfigResolved, None] | Tuple[None, str]:
    expr = f.underscore_expression
    if not isinstance(expr, UnderscoreCall):
        return None, "missing function call"

    call_expr = expr
    if len(call_expr._chalk__args) > 0 or len(call_expr._chalk__kwargs) > 0:  # pyright: ignore[reportPrivateUsage]
        return None, "should not have any arguments or keyword arguments"

    function_attribute = call_expr._chalk__parent  # pyright: ignore[reportPrivateUsage]
    if not isinstance(function_attribute, UnderscoreAttr):
        return None, "expected an aggregation, like `.sum()`"

    aggregation = function_attribute._chalk__attr  # pyright: ignore[reportPrivateUsage]
    if aggregation not in supported_aggs:
        return None, f"aggregation should be one of {', '.join(supported_aggs)}"

    aggregated_value = None
    getitem_expression = function_attribute._chalk__parent  # pyright: ignore[reportPrivateUsage]
    if isinstance(getitem_expression, UnderscoreItem):
        got_item = getitem_expression._chalk__key  # pyright: ignore[reportPrivateUsage]
        if not isinstance(got_item, UnderscoreAttr):
            return None, f"missing attribute to aggregate, e.g. `_.a[_.amount].{aggregation}()`"

        aggregated_value = got_item._chalk__attr  # pyright: ignore[reportPrivateUsage]
        if not isinstance(got_item._chalk__parent, UnderscoreRoot):  # pyright: ignore[reportPrivateUsage]
            return None, "expected a single feature from the child namespace, like `_.b`"
        child_attr_expression = getitem_expression._chalk__parent  # pyright: ignore[reportPrivateUsage]
    elif aggregation == "count":
        child_attr_expression = getitem_expression
    else:
        return None, f"missing attribute to aggregate, e.g. `_.a[_.amount].{aggregation}()`"

    if not isinstance(child_attr_expression, UnderscoreAttr):
        return None, f"expected reference to has-many feature, like _.children[...].{aggregation}()`"

    child_attr_name = child_attr_expression._chalk__attr  # pyright: ignore[reportPrivateUsage]
    if not isinstance(child_attr_expression._chalk__parent, UnderscoreRoot):  # pyright: ignore[reportPrivateUsage]
        return None, f"expected single feature of the child namespace, like `_.{child_attr_name}`"

    try:
        has_many_feature = getattr(f.features_cls, child_attr_name)
    except Exception:
        return None, f"could not find feature '{child_attr_name}' in the child namespace"

    underlying = unwrap_feature(has_many_feature, raise_error=False)

    if not isinstance(underlying, Feature):
        return None, f"the attribute '{child_attr_name}' is not a feature"

    if not underlying.is_has_many:
        return None, f"the attribute '{child_attr_name}' is not a has-many feature"

    joined_class = underlying.joined_class
    if joined_class is None:
        return None, f"has-many feature '{child_attr_name}' is not joined to a class"

    this_annotation = f.typ.parsed_annotation
    if aggregated_value is None:
        if aggregation != "count":
            return (
                None,
                f"feature '{f.window_stem}' does not aggregate a child feature; expected 'count' aggregation",
            )

        if this_annotation not in (int, float):
            return (
                None,
                f"feature '{f.window_stem}' should be a 'int' or 'float' for 'count' aggregation; found '{this_annotation.__name__}'",
            )
        return (
            WindowConfigResolved(
                bucket_duration_seconds=get_duration_secs(
                    f.window_materialization.get("bucket_duration", 60) if f.window_materialization is not None else 60
                ),
                child_feature=None,
                aggregation=aggregation,
            ),
            None,
        )

    joined_feature_wrapper = getattr(joined_class, aggregated_value, None)
    if joined_feature_wrapper is None:
        return None, f"joined class '{joined_class.__name__}' missing feature '{aggregated_value}'"

    joined_feature = unwrap_feature(joined_feature_wrapper)
    if not joined_feature.is_scalar:
        return None, f"joined feature '{joined_feature.window_stem}' not a scalar, like a 'float' or an 'int'"

    joined_annotation = joined_feature.typ.parsed_annotation

    if aggregation != "count":
        if joined_annotation is not float and joined_annotation is not int:
            return (
                None,
                f"joined feature '{joined_feature.window_stem}' should 'float' or 'int'; found '{joined_feature.typ.parsed_annotation.__name__}'",
            )

    if aggregation == "std" or aggregation == "var" or aggregation == "mean":
        if this_annotation != float:
            return (
                None,
                f"feature '{f.window_stem}' should be a 'float' for '{aggregation}' aggregation; found '{this_annotation.__name__}'",
            )

    elif aggregation == "min" or aggregation == "max":
        if this_annotation != joined_annotation:
            return (
                None,
                f"feature '{f.window_stem}' of type '{this_annotation.__name__}' should match joined feature '{joined_feature.name}' of type '{joined_annotation.__name__}' for '{aggregation}' aggregation",
            )

    elif aggregation == "count":
        if this_annotation not in (int, float):
            return (
                None,
                f"feature '{f.window_stem}' should be a 'int' or 'float' for 'count' aggregation; found '{this_annotation.__name__}'",
            )

    elif aggregation == "sum":
        if this_annotation not in (int, float):
            return (
                None,
                f"feature '{f.window_stem}' should be a 'int' or 'float' for 'sum' aggregation; found '{this_annotation.__name__}'",
            )
        if joined_annotation is float and this_annotation is int:
            return (
                None,
                f"feature '{f.window_stem}' should be a 'float' for 'sum' aggregation with joined feature '{joined_feature.name}'; found 'int'",
            )

    return (
        WindowConfigResolved(
            bucket_duration_seconds=get_duration_secs(
                f.window_materialization.get("bucket_duration", 60) if f.window_materialization is not None else 60
            ),
            child_feature=joined_feature,
            aggregation=aggregation,
        ),
        None,
    )


def import_all_files(
    file_allowlist: Optional[List[str]] = None,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
    check_ignores: bool = True,
    override: bool = False,
) -> List[FailedImport]:
    if project_root is None:
        project_root = get_directory_root()
    if project_root is None:
        return [
            FailedImport(
                filename="",
                module="",
                traceback="Could not find chalk.yaml in this directory or any parent directory",
            )
        ]

    python_files = None
    chalk_sql_files = None

    if file_allowlist is not None:
        python_files = []
        chalk_sql_files = []
        for f in file_allowlist:
            if f.endswith(".py"):
                python_files.append(Path(f))
            elif f.endswith(".chalk.sql"):
                chalk_sql_files.append(f)

    if only_sql_files:
        return import_sql_file_resolvers(project_root, chalk_sql_files, override=override)

    failed_imports: List[FailedImport] = import_all_python_files_from_dir(
        project_root=project_root,
        file_allowlist=python_files,
        check_ignores=check_ignores,
    )
    has_import_errors = len(failed_imports) > 0
    failed_imports.extend(
        import_sql_file_resolvers(
            path=project_root,
            file_allowlist=chalk_sql_files,
            has_import_errors=has_import_errors,
            override=override,
        )
    )

    for _, v in FeatureSetBase.registry.items():
        for f in v.__chalk_materialized_windows__:
            assert f.underscore_expression is not None
            assert f.window_materialization is not None

            mat, error = parse_windowed_materialization(f=f)

            if error is not None:
                f.lsp_error_builder.add_diagnostic(
                    message=f"The windowed materialization on feature '{f.window_stem}' is incorrectly configured.",
                    label=error,
                    range=f.lsp_error_builder.property_value_kwarg_range(
                        feature_name=f.window_stem,
                        kwarg="expression",
                    )
                    or f.lsp_error_builder.property_range(feature_name=f.window_stem),
                    code="39",
                )
            else:
                f.window_materialization_parsed = mat

    return failed_imports


def import_sql_file_resolvers(
    path: Path,
    file_allowlist: Optional[List[str]] = None,
    has_import_errors: bool = False,
    override: bool = False,
):
    if file_allowlist is not None:
        sql_resolver_results = get_sql_file_resolvers_from_paths(
            sources=BaseSQLSource.registry,
            paths=file_allowlist,
            has_import_errors=has_import_errors,
        )
    else:
        sql_resolver_results = get_sql_file_resolvers(
            sql_file_resolve_location=path,
            sources=BaseSQLSource.registry,
            has_import_errors=has_import_errors,
        )
    failed_imports: List[FailedImport] = []
    for result in sql_resolver_results:
        if result.resolver:
            result.resolver.add_to_registry(override=override)
        if result.errors:
            for error in result.errors:
                failed_imports.append(
                    FailedImport(
                        traceback=f"""EXCEPTION in Chalk SQL file resolver '{error.path}':
    {error.display}
""",
                        filename=error.path,
                        module=error.path,
                    )
                )
    return failed_imports


def get_resolver(
    resolver_fqn_or_name: str,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
) -> Resolver:
    """
    Returns a resolver by name or fqn, including sql file resolvers.

    Parameters
    ----------
    resolver_fqn_or_name: a string fqn or name of a resolver.
    Can also be a filename of sql file resolver
    project_root: an optional path to import sql file resolvers from.
    If not supplied, will select the root directory of the Chalk project.
    only_sql_files: if you have already imported all your features, sources, and resolvers, this flag
    can be used to restrict file search to sql file resolvers.

    Returns
    -------
    Resolver
    """
    failed_imports = import_all_files_once(project_root=project_root, only_sql_files=only_sql_files)
    if failed_imports:
        raise ValueError(f"File imports failed: {failed_imports}")
    if resolver_fqn_or_name.endswith(".chalk.sql"):
        resolver_fqn_or_name = resolver_fqn_or_name[: -len(".chalk.sql")]
    maybe_resolver = RESOLVER_REGISTRY.get_resolver(resolver_fqn_or_name)
    if maybe_resolver is not None:
        return maybe_resolver
    raise ValueError(f"No resolver with fqn or name {resolver_fqn_or_name} found")


def _get_py_files_fast(
    resolved_root: Path,
    venv_path: Optional[Path],
    ignore_config: Optional[IgnoreConfig],
) -> Iterable[Path]:
    """
    Gets all the .py files in the resolved_root directory and its subdirectories.
    Faster than the old method we were using because we are skipping the entire
    directory if the directory is determined to be ignored. But if any .gitignore
    or any .chalkignore file has negation, we revert to checking every filepath
    against each .*ignore file.

    :param resolved_root: Project root absolute path
    :param venv_path: Path of the venv folder to skip importing from.
    :param ignore_config: An optional CombinedIgnoreConfig object. If None, we simply don't check for ignores.
    :return: An iterable of Path each representing a .py file
    """

    for dirpath_str, dirnames, filenames in os.walk(resolved_root):
        dirpath = Path(dirpath_str).resolve()

        if (venv_path is not None and venv_path.samefile(dirpath)) or (
            ignore_config
            and not ignore_config.has_negation
            and ignore_config.ignored(os.path.join(str(dirpath), "#"))
            # Hack to make "dir/**" match "/Users/home/dir"
        ):
            dirnames.clear()  # Skip subdirectories
            continue  # Skip files

        for filename in filenames:
            if filename.endswith(".py"):
                filepath = dirpath / filename
                if not ignore_config or not ignore_config.ignored(filepath):
                    yield filepath


CHALK_IMPORT_FLAG: ContextVar[bool] = ContextVar("CHALK_IMPORT_FLAG", default=False)
""" A env var flag to be set to a truthy value during import to catch unsafe operations like ChalkClient().query()
Methods like that should check this env var flag and raise if run inappropriately """


class ChalkImporter:
    def __init__(self):
        super().__init__()
        self.errors: Dict[str, FailedImport] = {}
        self.ranges: Dict[str, RangeGQL] = {}
        self.short_tracebacks: Dict[str, str] = {}
        self.repo_files = None

    def add_repo_files(self, repo_files: List[Path]):
        self.repo_files = repo_files

    def add_error(
        self,
        ex_type: Type[BaseException],
        ex_value: BaseException,
        ex_traceback: TracebackType,
        filename: Path,
        module_path: str,
    ):
        tb = traceback.extract_tb(ex_traceback)
        frame = 0
        error_file = str(filename)
        line_number = None
        for i, tb_frame in enumerate(tb):
            tb_filepath = Path(tb_frame.filename).resolve()
            if self.repo_files and tb_filepath in self.repo_files:
                line_number = tb_frame.lineno
                error_file = tb_frame.filename
            if filename == Path(tb_frame.filename).resolve():
                frame = i
        if error_file in self.errors:
            return
        error_message = f"""EXCEPTION in module '{module_path}', file '{error_file}'{f", line {line_number}" if line_number else ""}"""
        full_traceback = f"""{error_message}:
{os.linesep.join(traceback.format_tb(ex_traceback)[frame:])}
{ex_type and ex_type.__name__}: {str(ex_value)}
"""
        self.errors[error_file] = FailedImport(
            traceback=full_traceback,
            filename=str(filename),
            module=module_path,
        )
        if line_number is not None:
            line = linecache.getline(str(filename), line_number)
            if line != "":
                self.ranges[error_file] = RangeGQL(
                    start=PositionGQL(
                        line=line_number,
                        character=len(line) - len(line.lstrip()),
                    ),
                    end=PositionGQL(
                        line=line_number,
                        character=len(line) - 1 if line is not None else 0,
                    ),
                )
                self.short_tracebacks[error_file] = error_message

    def get_failed_imports(self) -> List[FailedImport]:
        return list(self.errors.values())

    def convert_to_diagnostic(self, failed_import: FailedImport) -> Union[PublishDiagnosticsParams, None]:
        if failed_import.filename == "" or failed_import.filename not in self.ranges:
            return None

        range_ = self.ranges[failed_import.filename]
        traceback_ = self.errors[failed_import.filename].traceback
        builder = DiagnosticBuilder(
            severity=DiagnosticSeverityGQL.Error,
            message=traceback_,
            uri=failed_import.filename,
            range=range_,
            label="failed import",
            code="0",
            code_href=None,
        )
        return PublishDiagnosticsParams(
            uri=failed_import.filename,
            diagnostics=[builder.diagnostic],
        )

    def supplement_diagnostics(
        self, failed_imports: List[FailedImport], diagnostics: List[PublishDiagnosticsParams]
    ) -> List[PublishDiagnosticsParams]:
        diagnostic_uris = {diagnostic.uri for diagnostic in diagnostics}
        for failed_import in failed_imports:
            if failed_import.filename not in diagnostic_uris:
                diagnostic_or_none = self.convert_to_diagnostic(failed_import)
                if diagnostic_or_none is not None:
                    diagnostics.append(diagnostic_or_none)
        return diagnostics


CHALK_IMPORTER = ChalkImporter()


def import_all_python_files_from_dir(
    project_root: Path,
    check_ignores: bool = True,
    file_allowlist: Optional[List[Path]] = None,
) -> List[FailedImport]:
    use_old_ignores_check = env_var_bool("USE_OLD_IGNORES_CHECK")
    project_root = project_root.absolute()

    cwd = os.getcwd()
    os.chdir(project_root)
    # If we don't import both of these, we get in trouble.
    repo_root = Path(project_root)
    resolved_root = repo_root.resolve()
    _logger.debug(f"REPO_ROOT: {resolved_root}")
    sys.path.insert(0, str(resolved_root))
    sys.path.insert(0, str(repo_root.parent.resolve()))
    # Due to the path modifications above, we might have already imported
    # some files under a different module name, and Python doesn't detect
    # duplicate inputs of the same filename under different module names.
    # We can manually detect this by building a set of all absolute
    # filepaths we imported, and then comparing filepaths against this
    # set before attempting to import the module again.
    already_imported_files = {
        Path(v.__file__).resolve(): k
        for (k, v) in sys.modules.copy().items()
        if hasattr(v, "__file__") and isinstance(v.__file__, str)
    }
    token = CHALK_IMPORT_FLAG.set(True)
    try:
        venv = os.environ.get("VIRTUAL_ENV")
        if file_allowlist is not None:
            repo_files = file_allowlist
        elif use_old_ignores_check:
            ignore_functions: List[Callable[[Union[Path, str]], bool]] = []
            ignore_functions.extend(
                parse_gitignore(str(x))[0] for x in search_recursively_for_file(project_root, ".gitignore")
            )
            ignore_functions.extend(
                parse_gitignore(str(x))[0] for x in search_recursively_for_file(project_root, ".chalkignore")
            )

            repo_files = {p.resolve() for p in repo_root.glob(os.path.join("**", "*.py")) if p.is_file()}
            repo_files = sorted(repo_files)
            repo_files = list(
                repo_file for repo_file in repo_files if venv is None or Path(venv) not in repo_file.parents
            )
            if check_ignores:
                repo_files = list(p for p in repo_files if not is_ignored(p, ignore_functions))
        else:
            venv_path = None if venv is None else Path(venv)
            ignore_config = get_default_combined_ignore_config(resolved_root) if check_ignores else None
            repo_files = list(
                _get_py_files_fast(resolved_root=resolved_root, venv_path=venv_path, ignore_config=ignore_config)
            )

        CHALK_IMPORTER.add_repo_files(repo_files)
        for filename in repo_files:
            # we want resolved_root in case repo_root contains a symlink
            if filename in already_imported_files:
                _logger.debug(
                    f"Skipping import of '{filename}' since it is already imported as module {already_imported_files[filename]}"
                )
                continue
            module_path = _py_path_to_module(filename, resolved_root)
            if module_path.startswith(".eggs") or module_path.startswith("venv") or filename.name == "setup.py":
                continue
            try:
                importlib.import_module(module_path)
            except Exception as e:
                if not LSPErrorBuilder.promote_exception(e):
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    assert ex_type is not None
                    assert ex_value is not None
                    assert ex_traceback is not None
                    CHALK_IMPORTER.add_error(ex_type, ex_value, ex_traceback, filename, module_path)
                    _logger.debug(f"Failed while importing {module_path}", exc_info=True)
            else:
                _logger.debug(f"Imported '{filename}' as module {module_path}")
                already_imported_files[filename] = module_path
    finally:
        CHALK_IMPORT_FLAG.reset(token)
        # Let's remove our added entries in sys.path so we don't pollute it
        sys.path.pop(0)
        sys.path.pop(0)
        # And let's go back to our original directory
        os.chdir(cwd)
    return CHALK_IMPORTER.get_failed_imports()
