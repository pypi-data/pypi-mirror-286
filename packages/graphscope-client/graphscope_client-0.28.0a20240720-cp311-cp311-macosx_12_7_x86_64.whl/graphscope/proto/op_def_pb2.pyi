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

import attr_value_pb2
import builtins
import collections.abc
import error_codes_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import graph_def_pb2
import types_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class OpDef(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class AttrEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.int
        @property
        def value(self) -> attr_value_pb2.AttrValue: ...
        def __init__(
            self,
            *,
            key: builtins.int = ...,
            value: attr_value_pb2.AttrValue | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    OP_FIELD_NUMBER: builtins.int
    PARENTS_FIELD_NUMBER: builtins.int
    OUTPUT_TYPE_FIELD_NUMBER: builtins.int
    ATTR_FIELD_NUMBER: builtins.int
    LARGE_ATTR_FIELD_NUMBER: builtins.int
    QUERY_ARGS_FIELD_NUMBER: builtins.int
    key: builtins.str
    """Unique key for every OpDef. Usually generated by analytical engine."""
    op: types_pb2.OperationType.ValueType
    """The operation name. There may be custom parameters in attrs."""
    output_type: types_pb2.OutputType.ValueType
    """Different types of op may create different output."""
    @property
    def parents(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Used for store an op's parents, i.e. use which op to produce this op."""

    @property
    def attr(self) -> google.protobuf.internal.containers.MessageMap[builtins.int, attr_value_pb2.AttrValue]:
        """Operation-specific configuration."""

    @property
    def large_attr(self) -> attr_value_pb2.LargeAttrValue:
        """Operation-specific configuration for large chunk.
        e.g. dataframe or numpy data
        """

    @property
    def query_args(self) -> types_pb2.QueryArgs:
        """arguments that served as application querying parameters.
        Such as source vertex id for SSSP.
        """

    def __init__(
        self,
        *,
        key: builtins.str = ...,
        op: types_pb2.OperationType.ValueType = ...,
        parents: collections.abc.Iterable[builtins.str] | None = ...,
        output_type: types_pb2.OutputType.ValueType = ...,
        attr: collections.abc.Mapping[builtins.int, attr_value_pb2.AttrValue] | None = ...,
        large_attr: attr_value_pb2.LargeAttrValue | None = ...,
        query_args: types_pb2.QueryArgs | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["large_attr", b"large_attr", "query_args", b"query_args"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["attr", b"attr", "key", b"key", "large_attr", b"large_attr", "op", b"op", "output_type", b"output_type", "parents", b"parents", "query_args", b"query_args"]) -> None: ...

global___OpDef = OpDef

@typing.final
class OpResult(google.protobuf.message.Message):
    """Result of Op"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Meta(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        METRICS_FIELD_NUMBER: builtins.int
        HAS_LARGE_RESULT_FIELD_NUMBER: builtins.int
        metrics: builtins.str
        """if success, store the metrics. (e.g. how many seconds used, memory bytes...)"""
        has_large_result: builtins.bool
        """result represents raw bytes if:
         1) NDArray or DataFrame
         2) Gremlin result
         3) Graph report information of Networkx
        """
        def __init__(
            self,
            *,
            metrics: builtins.str = ...,
            has_large_result: builtins.bool = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["has_large_result", b"has_large_result", "metrics", b"metrics"]) -> None: ...

    CODE_FIELD_NUMBER: builtins.int
    KEY_FIELD_NUMBER: builtins.int
    META_FIELD_NUMBER: builtins.int
    RESULT_FIELD_NUMBER: builtins.int
    ERROR_MSG_FIELD_NUMBER: builtins.int
    GRAPH_DEF_FIELD_NUMBER: builtins.int
    code: error_codes_pb2.Code.ValueType
    """Status code"""
    key: builtins.str
    """unique key for every op"""
    result: builtins.bytes
    """result represents app_name or context_key or raw bytes If the op returns a NDArray or DataFrame"""
    error_msg: builtins.str
    @property
    def meta(self) -> global___OpResult.Meta:
        """Meta"""

    @property
    def graph_def(self) -> graph_def_pb2.GraphDefPb: ...
    def __init__(
        self,
        *,
        code: error_codes_pb2.Code.ValueType = ...,
        key: builtins.str = ...,
        meta: global___OpResult.Meta | None = ...,
        result: builtins.bytes = ...,
        error_msg: builtins.str = ...,
        graph_def: graph_def_pb2.GraphDefPb | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["graph_def", b"graph_def", "meta", b"meta"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["code", b"code", "error_msg", b"error_msg", "graph_def", b"graph_def", "key", b"key", "meta", b"meta", "result", b"result"]) -> None: ...

global___OpResult = OpResult

@typing.final
class DagDef(google.protobuf.message.Message):
    """Consist by list of ops."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OP_FIELD_NUMBER: builtins.int
    @property
    def op(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OpDef]: ...
    def __init__(
        self,
        *,
        op: collections.abc.Iterable[global___OpDef] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["op", b"op"]) -> None: ...

global___DagDef = DagDef
