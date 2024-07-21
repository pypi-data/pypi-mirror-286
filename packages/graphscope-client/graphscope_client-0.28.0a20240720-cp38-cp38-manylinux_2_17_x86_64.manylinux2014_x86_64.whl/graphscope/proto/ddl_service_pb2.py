# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ddl_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import graph_def_pb2 as graph__def__pb2
try:
  schema__common__pb2 = graph__def__pb2.schema__common__pb2
except AttributeError:
  schema__common__pb2 = graph__def__pb2.schema_common_pb2
import schema_common_pb2 as schema__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x64\x64l_service.proto\x12\x0cgs.rpc.groot\x1a\x0fgraph_def.proto\x1a\x13schema_common.proto\"\xfd\x05\n\x12\x42\x61tchSubmitRequest\x12\x16\n\x0e\x66ormat_version\x18\x01 \x01(\x05\x12\x17\n\x0fsimple_response\x18\x02 \x01(\x08\x12:\n\x05value\x18\x03 \x03(\x0b\x32+.gs.rpc.groot.BatchSubmitRequest.DDLRequest\x1a\xf9\x04\n\nDDLRequest\x12K\n\x1a\x63reate_vertex_type_request\x18\x01 \x01(\x0b\x32%.gs.rpc.groot.CreateVertexTypeRequestH\x00\x12G\n\x18\x63reate_edge_type_request\x18\x02 \x01(\x0b\x32#.gs.rpc.groot.CreateEdgeTypeRequestH\x00\x12\x41\n\x15\x61\x64\x64_edge_kind_request\x18\x03 \x01(\x0b\x32 .gs.rpc.groot.AddEdgeKindRequestH\x00\x12G\n\x18remove_edge_kind_request\x18\x04 \x01(\x0b\x32#.gs.rpc.groot.RemoveEdgeKindRequestH\x00\x12G\n\x18\x64rop_vertex_type_request\x18\x05 \x01(\x0b\x32#.gs.rpc.groot.DropVertexTypeRequestH\x00\x12\x43\n\x16\x64rop_edge_type_request\x18\x06 \x01(\x0b\x32!.gs.rpc.groot.DropEdgeTypeRequestH\x00\x12Z\n\"add_vertex_type_properties_request\x18\x07 \x01(\x0b\x32,.gs.rpc.groot.AddVertexTypePropertiesRequestH\x00\x12V\n add_edge_type_properties_request\x18\x08 \x01(\x0b\x32*.gs.rpc.groot.AddEdgeTypePropertiesRequestH\x00\x42\x07\n\x05value\"Z\n\x13\x42\x61tchSubmitResponse\x12\x16\n\x0e\x66ormat_version\x18\x01 \x01(\x05\x12+\n\tgraph_def\x18\x02 \x01(\x0b\x32\x18.gs.rpc.graph.GraphDefPb\"D\n\x17\x43reateVertexTypeRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"K\n\x1e\x41\x64\x64VertexTypePropertiesRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"B\n\x15\x43reateEdgeTypeRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"I\n\x1c\x41\x64\x64\x45\x64geTypePropertiesRequest\x12)\n\x08type_def\x18\x01 \x01(\x0b\x32\x17.gs.rpc.graph.TypeDefPb\"\\\n\x12\x41\x64\x64\x45\x64geKindRequest\x12\x12\n\nedge_label\x18\x01 \x01(\t\x12\x18\n\x10src_vertex_label\x18\x02 \x01(\t\x12\x18\n\x10\x64st_vertex_label\x18\x03 \x01(\t\"_\n\x15RemoveEdgeKindRequest\x12\x12\n\nedge_label\x18\x01 \x01(\t\x12\x18\n\x10src_vertex_label\x18\x02 \x01(\t\x12\x18\n\x10\x64st_vertex_label\x18\x03 \x01(\t\"&\n\x15\x44ropVertexTypeRequest\x12\r\n\x05label\x18\x01 \x01(\t\"$\n\x13\x44ropEdgeTypeRequest\x12\r\n\x05label\x18\x01 \x01(\t\"!\n\x12GetGraphDefRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"B\n\x13GetGraphDefResponse\x12+\n\tgraph_def\x18\x01 \x01(\x0b\x32\x18.gs.rpc.graph.GraphDefPb2\xb9\x01\n\x0fGrootDdlService\x12R\n\x0b\x62\x61tchSubmit\x12 .gs.rpc.groot.BatchSubmitRequest\x1a!.gs.rpc.groot.BatchSubmitResponse\x12R\n\x0bgetGraphDef\x12 .gs.rpc.groot.GetGraphDefRequest\x1a!.gs.rpc.groot.GetGraphDefResponseB&\n\"com.alibaba.graphscope.proto.grootP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ddl_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.alibaba.graphscope.proto.grootP\001'
  _globals['_BATCHSUBMITREQUEST']._serialized_start=74
  _globals['_BATCHSUBMITREQUEST']._serialized_end=839
  _globals['_BATCHSUBMITREQUEST_DDLREQUEST']._serialized_start=206
  _globals['_BATCHSUBMITREQUEST_DDLREQUEST']._serialized_end=839
  _globals['_BATCHSUBMITRESPONSE']._serialized_start=841
  _globals['_BATCHSUBMITRESPONSE']._serialized_end=931
  _globals['_CREATEVERTEXTYPEREQUEST']._serialized_start=933
  _globals['_CREATEVERTEXTYPEREQUEST']._serialized_end=1001
  _globals['_ADDVERTEXTYPEPROPERTIESREQUEST']._serialized_start=1003
  _globals['_ADDVERTEXTYPEPROPERTIESREQUEST']._serialized_end=1078
  _globals['_CREATEEDGETYPEREQUEST']._serialized_start=1080
  _globals['_CREATEEDGETYPEREQUEST']._serialized_end=1146
  _globals['_ADDEDGETYPEPROPERTIESREQUEST']._serialized_start=1148
  _globals['_ADDEDGETYPEPROPERTIESREQUEST']._serialized_end=1221
  _globals['_ADDEDGEKINDREQUEST']._serialized_start=1223
  _globals['_ADDEDGEKINDREQUEST']._serialized_end=1315
  _globals['_REMOVEEDGEKINDREQUEST']._serialized_start=1317
  _globals['_REMOVEEDGEKINDREQUEST']._serialized_end=1412
  _globals['_DROPVERTEXTYPEREQUEST']._serialized_start=1414
  _globals['_DROPVERTEXTYPEREQUEST']._serialized_end=1452
  _globals['_DROPEDGETYPEREQUEST']._serialized_start=1454
  _globals['_DROPEDGETYPEREQUEST']._serialized_end=1490
  _globals['_GETGRAPHDEFREQUEST']._serialized_start=1492
  _globals['_GETGRAPHDEFREQUEST']._serialized_end=1525
  _globals['_GETGRAPHDEFRESPONSE']._serialized_start=1527
  _globals['_GETGRAPHDEFRESPONSE']._serialized_end=1593
  _globals['_GROOTDDLSERVICE']._serialized_start=1596
  _globals['_GROOTDDLSERVICE']._serialized_end=1781
# @@protoc_insertion_point(module_scope)
