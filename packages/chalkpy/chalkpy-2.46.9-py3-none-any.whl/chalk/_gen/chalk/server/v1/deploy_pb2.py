# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/deploy.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.auth.v1 import audit_pb2 as chalk_dot_auth_dot_v1_dot_audit__pb2
from chalk._gen.chalk.auth.v1 import (
    permissions_pb2 as chalk_dot_auth_dot_v1_dot_permissions__pb2,
)
from chalk._gen.chalk.server.v1 import (
    deployment_pb2 as chalk_dot_server_dot_v1_dot_deployment__pb2,
)


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1c\x63halk/server/v1/deploy.proto\x12\x0f\x63halk.server.v1\x1a\x19\x63halk/auth/v1/audit.proto\x1a\x1f\x63halk/auth/v1/permissions.proto\x1a chalk/server/v1/deployment.proto"\x97\x01\n\x13\x44\x65ployBranchRequest\x12\x1f\n\x0b\x62ranch_name\x18\x01 \x01(\tR\nbranchName\x12!\n\x0creset_branch\x18\x02 \x01(\x08R\x0bresetBranch\x12\x18\n\x07\x61rchive\x18\x03 \x01(\x0cR\x07\x61rchive\x12"\n\ris_hot_deploy\x18\x04 \x01(\x08R\x0bisHotDeploy";\n\x14\x44\x65ployBranchResponse\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId";\n\x14GetDeploymentRequest\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId"T\n\x15GetDeploymentResponse\x12;\n\ndeployment\x18\x01 \x01(\x0b\x32\x1b.chalk.server.v1.DeploymentR\ndeployment"\x18\n\x16ListDeploymentsRequest"X\n\x17ListDeploymentsResponse\x12=\n\x0b\x64\x65ployments\x18\x01 \x03(\x0b\x32\x1b.chalk.server.v1.DeploymentR\x0b\x64\x65ployments"?\n\x18SuspendDeploymentRequest\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId"X\n\x19SuspendDeploymentResponse\x12;\n\ndeployment\x18\x01 \x01(\x0b\x32\x1b.chalk.server.v1.DeploymentR\ndeployment"v\n\x16ScaleDeploymentRequest\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId\x12\x37\n\x06sizing\x18\x02 \x01(\x0b\x32\x1f.chalk.server.v1.InstanceSizingR\x06sizing"V\n\x17ScaleDeploymentResponse\x12;\n\ndeployment\x18\x01 \x01(\x0b\x32\x1b.chalk.server.v1.DeploymentR\ndeployment"M\n\x14TagDeploymentRequest\x12#\n\rdeployment_id\x18\x01 \x01(\tR\x0c\x64\x65ploymentId\x12\x10\n\x03tag\x18\x02 \x01(\tR\x03tag"\xaa\x01\n\x15TagDeploymentResponse\x12;\n\ndeployment\x18\x01 \x01(\x0b\x32\x1b.chalk.server.v1.DeploymentR\ndeployment\x12\x39\n\x16untagged_deployment_id\x18\x02 \x01(\tH\x00R\x14untaggedDeploymentId\x88\x01\x01\x42\x19\n\x17_untagged_deployment_id2\x94\x05\n\rDeployService\x12`\n\x0c\x44\x65ployBranch\x12$.chalk.server.v1.DeployBranchRequest\x1a%.chalk.server.v1.DeployBranchResponse"\x03\x80}\r\x12\x63\n\rGetDeployment\x12%.chalk.server.v1.GetDeploymentRequest\x1a&.chalk.server.v1.GetDeploymentResponse"\x03\x80}\x0b\x12i\n\x0fListDeployments\x12\'.chalk.server.v1.ListDeploymentsRequest\x1a(.chalk.server.v1.ListDeploymentsResponse"\x03\x80}\x0b\x12u\n\x11SuspendDeployment\x12).chalk.server.v1.SuspendDeploymentRequest\x1a*.chalk.server.v1.SuspendDeploymentResponse"\t\x80}\x0c\x8a\xd3\x0e\x02\x08\x02\x12o\n\x0fScaleDeployment\x12\'.chalk.server.v1.ScaleDeploymentRequest\x1a(.chalk.server.v1.ScaleDeploymentResponse"\t\x80}\x0c\x8a\xd3\x0e\x02\x08\x02\x12i\n\rTagDeployment\x12%.chalk.server.v1.TagDeploymentRequest\x1a&.chalk.server.v1.TagDeploymentResponse"\t\x80}\x0c\x8a\xd3\x0e\x02\x08\x02\x42\x94\x01\n\x13\x63om.chalk.server.v1B\x0b\x44\x65ployProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "chalk.server.v1.deploy_pb2", _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\013DeployProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_DEPLOYSERVICE"].methods_by_name["DeployBranch"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "DeployBranch"
    ]._serialized_options = b"\200}\r"
    _globals["_DEPLOYSERVICE"].methods_by_name["GetDeployment"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "GetDeployment"
    ]._serialized_options = b"\200}\013"
    _globals["_DEPLOYSERVICE"].methods_by_name["ListDeployments"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "ListDeployments"
    ]._serialized_options = b"\200}\013"
    _globals["_DEPLOYSERVICE"].methods_by_name["SuspendDeployment"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "SuspendDeployment"
    ]._serialized_options = b"\200}\014\212\323\016\002\010\002"
    _globals["_DEPLOYSERVICE"].methods_by_name["ScaleDeployment"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "ScaleDeployment"
    ]._serialized_options = b"\200}\014\212\323\016\002\010\002"
    _globals["_DEPLOYSERVICE"].methods_by_name["TagDeployment"]._options = None
    _globals["_DEPLOYSERVICE"].methods_by_name[
        "TagDeployment"
    ]._serialized_options = b"\200}\014\212\323\016\002\010\002"
    _globals["_DEPLOYBRANCHREQUEST"]._serialized_start = 144
    _globals["_DEPLOYBRANCHREQUEST"]._serialized_end = 295
    _globals["_DEPLOYBRANCHRESPONSE"]._serialized_start = 297
    _globals["_DEPLOYBRANCHRESPONSE"]._serialized_end = 356
    _globals["_GETDEPLOYMENTREQUEST"]._serialized_start = 358
    _globals["_GETDEPLOYMENTREQUEST"]._serialized_end = 417
    _globals["_GETDEPLOYMENTRESPONSE"]._serialized_start = 419
    _globals["_GETDEPLOYMENTRESPONSE"]._serialized_end = 503
    _globals["_LISTDEPLOYMENTSREQUEST"]._serialized_start = 505
    _globals["_LISTDEPLOYMENTSREQUEST"]._serialized_end = 529
    _globals["_LISTDEPLOYMENTSRESPONSE"]._serialized_start = 531
    _globals["_LISTDEPLOYMENTSRESPONSE"]._serialized_end = 619
    _globals["_SUSPENDDEPLOYMENTREQUEST"]._serialized_start = 621
    _globals["_SUSPENDDEPLOYMENTREQUEST"]._serialized_end = 684
    _globals["_SUSPENDDEPLOYMENTRESPONSE"]._serialized_start = 686
    _globals["_SUSPENDDEPLOYMENTRESPONSE"]._serialized_end = 774
    _globals["_SCALEDEPLOYMENTREQUEST"]._serialized_start = 776
    _globals["_SCALEDEPLOYMENTREQUEST"]._serialized_end = 894
    _globals["_SCALEDEPLOYMENTRESPONSE"]._serialized_start = 896
    _globals["_SCALEDEPLOYMENTRESPONSE"]._serialized_end = 982
    _globals["_TAGDEPLOYMENTREQUEST"]._serialized_start = 984
    _globals["_TAGDEPLOYMENTREQUEST"]._serialized_end = 1061
    _globals["_TAGDEPLOYMENTRESPONSE"]._serialized_start = 1064
    _globals["_TAGDEPLOYMENTRESPONSE"]._serialized_end = 1234
    _globals["_DEPLOYSERVICE"]._serialized_start = 1237
    _globals["_DEPLOYSERVICE"]._serialized_end = 1897
# @@protoc_insertion_point(module_scope)
