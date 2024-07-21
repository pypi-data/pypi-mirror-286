"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import builtins
import collections.abc
import error_codes_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import op_def_pb2
import sys
import types_pb2
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _LearningBackend:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _LearningBackendEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_LearningBackend.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    GRAPHLEARN: _LearningBackend.ValueType  # 0
    GRAPHLEARN_TORCH: _LearningBackend.ValueType  # 1

class LearningBackend(_LearningBackend, metaclass=_LearningBackendEnumTypeWrapper): ...

GRAPHLEARN: LearningBackend.ValueType  # 0
GRAPHLEARN_TORCH: LearningBackend.ValueType  # 1
global___LearningBackend = LearningBackend

@typing.final
class ConnectSessionRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    ConnectSession method request/response protos.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CLEANUP_INSTANCE_FIELD_NUMBER: builtins.int
    DANGLING_TIMEOUT_SECONDS_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    RECONNECT_FIELD_NUMBER: builtins.int
    cleanup_instance: builtins.bool
    dangling_timeout_seconds: builtins.int
    version: builtins.str
    """check version compatibility"""
    reconnect: builtins.bool
    """Allow reusing existing session. Reusing would be useful for users when the
    client, e.g., jupyter-notebook losses the connection with the backend, but
    still want to reuse the _cluster_ resources, we should allow users to
    establish the RPC connection to reuse, without waiting for dangling timeout.

    See also #287 for more discussion about session persistence and restore.
    """
    def __init__(
        self,
        *,
        cleanup_instance: builtins.bool = ...,
        dangling_timeout_seconds: builtins.int = ...,
        version: builtins.str = ...,
        reconnect: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cleanup_instance", b"cleanup_instance", "dangling_timeout_seconds", b"dangling_timeout_seconds", "reconnect", b"reconnect", "version", b"version"]) -> None: ...

global___ConnectSessionRequest = ConnectSessionRequest

@typing.final
class ConnectSessionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    CLUSTER_TYPE_FIELD_NUMBER: builtins.int
    NUM_WORKERS_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    ENGINE_CONFIG_FIELD_NUMBER: builtins.int
    HOST_NAMES_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    """The session handle to be used in subsequent calls for the created session.

    The client must arrange to call CloseSession with this returned
    session handle to close the session.
    """
    cluster_type: types_pb2.ClusterType.ValueType
    num_workers: builtins.int
    namespace: builtins.str
    engine_config: builtins.str
    @property
    def host_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        cluster_type: types_pb2.ClusterType.ValueType = ...,
        num_workers: builtins.int = ...,
        namespace: builtins.str = ...,
        engine_config: builtins.str = ...,
        host_names: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cluster_type", b"cluster_type", "engine_config", b"engine_config", "host_names", b"host_names", "namespace", b"namespace", "num_workers", b"num_workers", "session_id", b"session_id"]) -> None: ...

global___ConnectSessionResponse = ConnectSessionResponse

@typing.final
class HeartBeatRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    HeartBeat method request/response protos.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["session_id", b"session_id"]) -> None: ...

global___HeartBeatRequest = HeartBeatRequest

@typing.final
class HeartBeatResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___HeartBeatResponse = HeartBeatResponse

@typing.final
class RunStepRequestHead(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    RunStep method request/response protos.

    In most case only the Head is used.
    When the content is very large, exceeding the hard message limit of GRPC,
    It will be split into chunks and be streamed by a Head followed by 1~n Bodies.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    DAG_DEF_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    """REQUIRED: session_id must be returned by a CreateSession call
    to the same master service.
    """
    @property
    def dag_def(self) -> op_def_pb2.DagDef:
        """REQUIRED: A Dag with op that will be evaluated."""

    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        dag_def: op_def_pb2.DagDef | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["dag_def", b"dag_def"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["dag_def", b"dag_def", "session_id", b"session_id"]) -> None: ...

global___RunStepRequestHead = RunStepRequestHead

@typing.final
class RunStepRequestBody(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CHUNK_FIELD_NUMBER: builtins.int
    OP_KEY_FIELD_NUMBER: builtins.int
    HAS_NEXT_FIELD_NUMBER: builtins.int
    chunk: builtins.bytes
    op_key: builtins.str
    has_next: builtins.bool
    def __init__(
        self,
        *,
        chunk: builtins.bytes = ...,
        op_key: builtins.str = ...,
        has_next: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["chunk", b"chunk", "has_next", b"has_next", "op_key", b"op_key"]) -> None: ...

global___RunStepRequestBody = RunStepRequestBody

@typing.final
class RunStepRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEAD_FIELD_NUMBER: builtins.int
    BODY_FIELD_NUMBER: builtins.int
    @property
    def head(self) -> global___RunStepRequestHead: ...
    @property
    def body(self) -> global___RunStepRequestBody: ...
    def __init__(
        self,
        *,
        head: global___RunStepRequestHead | None = ...,
        body: global___RunStepRequestBody | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["body", b"body", "head", b"head", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["body", b"body", "head", b"head", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["value", b"value"]) -> typing.Literal["head", "body"] | None: ...

global___RunStepRequest = RunStepRequest

@typing.final
class RunStepResponseHead(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESULTS_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    ERROR_MSG_FIELD_NUMBER: builtins.int
    FULL_EXCEPTION_FIELD_NUMBER: builtins.int
    code: error_codes_pb2.Code.ValueType
    error_msg: builtins.str
    full_exception: builtins.bytes
    @property
    def results(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[op_def_pb2.OpResult]:
        """list of result of ops in dag"""

    def __init__(
        self,
        *,
        results: collections.abc.Iterable[op_def_pb2.OpResult] | None = ...,
        code: error_codes_pb2.Code.ValueType = ...,
        error_msg: builtins.str = ...,
        full_exception: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["code", b"code", "error_msg", b"error_msg", "full_exception", b"full_exception", "results", b"results"]) -> None: ...

global___RunStepResponseHead = RunStepResponseHead

@typing.final
class RunStepResponseBody(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CHUNK_FIELD_NUMBER: builtins.int
    HAS_NEXT_FIELD_NUMBER: builtins.int
    chunk: builtins.bytes
    has_next: builtins.bool
    def __init__(
        self,
        *,
        chunk: builtins.bytes = ...,
        has_next: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["chunk", b"chunk", "has_next", b"has_next"]) -> None: ...

global___RunStepResponseBody = RunStepResponseBody

@typing.final
class RunStepResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEAD_FIELD_NUMBER: builtins.int
    BODY_FIELD_NUMBER: builtins.int
    @property
    def head(self) -> global___RunStepResponseHead: ...
    @property
    def body(self) -> global___RunStepResponseBody: ...
    def __init__(
        self,
        *,
        head: global___RunStepResponseHead | None = ...,
        body: global___RunStepResponseBody | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["body", b"body", "head", b"head", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["body", b"body", "head", b"head", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["value", b"value"]) -> typing.Literal["head", "body"] | None: ...

global___RunStepResponse = RunStepResponse

@typing.final
class FetchLogsRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    FetchLogs method request/response protos.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["session_id", b"session_id"]) -> None: ...

global___FetchLogsRequest = FetchLogsRequest

@typing.final
class FetchLogsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INFO_MESSAGE_FIELD_NUMBER: builtins.int
    ERROR_MESSAGE_FIELD_NUMBER: builtins.int
    info_message: builtins.str
    """log info."""
    error_message: builtins.str
    """log error."""
    def __init__(
        self,
        *,
        info_message: builtins.str = ...,
        error_message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["error_message", b"error_message", "info_message", b"info_message"]) -> None: ...

global___FetchLogsResponse = FetchLogsResponse

@typing.final
class CloseSessionRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    CloseSession method request/response protos.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    """REQUIRED: session_id must be returned by a CreateSession call
    to the same master service.
    """
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["session_id", b"session_id"]) -> None: ...

global___CloseSessionRequest = CloseSessionRequest

@typing.final
class CloseSessionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CloseSessionResponse = CloseSessionResponse

@typing.final
class AddLibRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    Upload libs/jars from client to pods

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    GAR_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    gar: builtins.bytes
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        gar: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["gar", b"gar", "session_id", b"session_id"]) -> None: ...

global___AddLibRequest = AddLibRequest

@typing.final
class AddLibResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___AddLibResponse = AddLibResponse

@typing.final
class CreateAnalyticalInstanceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["session_id", b"session_id"]) -> None: ...

global___CreateAnalyticalInstanceRequest = CreateAnalyticalInstanceRequest

@typing.final
class CreateAnalyticalInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INSTANCE_ID_FIELD_NUMBER: builtins.int
    ENGINE_CONFIG_FIELD_NUMBER: builtins.int
    HOST_NAMES_FIELD_NUMBER: builtins.int
    instance_id: builtins.str
    engine_config: builtins.str
    @property
    def host_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        instance_id: builtins.str = ...,
        engine_config: builtins.str = ...,
        host_names: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["engine_config", b"engine_config", "host_names", b"host_names", "instance_id", b"instance_id"]) -> None: ...

global___CreateAnalyticalInstanceResponse = CreateAnalyticalInstanceResponse

@typing.final
class CreateInteractiveInstanceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class ParamsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.str
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    SESSION_ID_FIELD_NUMBER: builtins.int
    OBJECT_ID_FIELD_NUMBER: builtins.int
    SCHEMA_PATH_FIELD_NUMBER: builtins.int
    PARAMS_FIELD_NUMBER: builtins.int
    WITH_CYPHER_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    object_id: builtins.int
    schema_path: builtins.str
    with_cypher: builtins.bool
    @property
    def params(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.str]: ...
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        object_id: builtins.int = ...,
        schema_path: builtins.str = ...,
        params: collections.abc.Mapping[builtins.str, builtins.str] | None = ...,
        with_cypher: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["object_id", b"object_id", "params", b"params", "schema_path", b"schema_path", "session_id", b"session_id", "with_cypher", b"with_cypher"]) -> None: ...

global___CreateInteractiveInstanceRequest = CreateInteractiveInstanceRequest

@typing.final
class CreateInteractiveInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    GREMLIN_ENDPOINT_FIELD_NUMBER: builtins.int
    CYPHER_ENDPOINT_FIELD_NUMBER: builtins.int
    OBJECT_ID_FIELD_NUMBER: builtins.int
    gremlin_endpoint: builtins.str
    cypher_endpoint: builtins.str
    object_id: builtins.int
    def __init__(
        self,
        *,
        gremlin_endpoint: builtins.str = ...,
        cypher_endpoint: builtins.str = ...,
        object_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["cypher_endpoint", b"cypher_endpoint", "gremlin_endpoint", b"gremlin_endpoint", "object_id", b"object_id"]) -> None: ...

global___CreateInteractiveInstanceResponse = CreateInteractiveInstanceResponse

@typing.final
class CreateLearningInstanceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    OBJECT_ID_FIELD_NUMBER: builtins.int
    HANDLE_FIELD_NUMBER: builtins.int
    CONFIG_FIELD_NUMBER: builtins.int
    LEARNING_BACKEND_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    object_id: builtins.int
    handle: builtins.str
    config: builtins.str
    learning_backend: global___LearningBackend.ValueType
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        object_id: builtins.int = ...,
        handle: builtins.str = ...,
        config: builtins.str = ...,
        learning_backend: global___LearningBackend.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["config", b"config", "handle", b"handle", "learning_backend", b"learning_backend", "object_id", b"object_id", "session_id", b"session_id"]) -> None: ...

global___CreateLearningInstanceRequest = CreateLearningInstanceRequest

@typing.final
class CreateLearningInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OBJECT_ID_FIELD_NUMBER: builtins.int
    HANDLE_FIELD_NUMBER: builtins.int
    CONFIG_FIELD_NUMBER: builtins.int
    ENDPOINTS_FIELD_NUMBER: builtins.int
    object_id: builtins.int
    handle: builtins.str
    config: builtins.str
    @property
    def endpoints(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        object_id: builtins.int = ...,
        handle: builtins.str = ...,
        config: builtins.str = ...,
        endpoints: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["config", b"config", "endpoints", b"endpoints", "handle", b"handle", "object_id", b"object_id"]) -> None: ...

global___CreateLearningInstanceResponse = CreateLearningInstanceResponse

@typing.final
class CloseAnalyticalInstanceRequest(google.protobuf.message.Message):
    """//////////////////////////////////////////////////////////////////////////////

    Close Instance request/response protos.

    //////////////////////////////////////////////////////////////////////////////
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    INSTANCE_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    instance_id: builtins.str
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        instance_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["instance_id", b"instance_id", "session_id", b"session_id"]) -> None: ...

global___CloseAnalyticalInstanceRequest = CloseAnalyticalInstanceRequest

@typing.final
class CloseAnalyticalInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CloseAnalyticalInstanceResponse = CloseAnalyticalInstanceResponse

@typing.final
class CloseInteractiveInstanceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    OBJECT_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    object_id: builtins.int
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        object_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["object_id", b"object_id", "session_id", b"session_id"]) -> None: ...

global___CloseInteractiveInstanceRequest = CloseInteractiveInstanceRequest

@typing.final
class CloseInteractiveInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CloseInteractiveInstanceResponse = CloseInteractiveInstanceResponse

@typing.final
class CloseLearningInstanceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_ID_FIELD_NUMBER: builtins.int
    OBJECT_ID_FIELD_NUMBER: builtins.int
    session_id: builtins.str
    object_id: builtins.int
    def __init__(
        self,
        *,
        session_id: builtins.str = ...,
        object_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["object_id", b"object_id", "session_id", b"session_id"]) -> None: ...

global___CloseLearningInstanceRequest = CloseLearningInstanceRequest

@typing.final
class CloseLearningInstanceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___CloseLearningInstanceResponse = CloseLearningInstanceResponse
