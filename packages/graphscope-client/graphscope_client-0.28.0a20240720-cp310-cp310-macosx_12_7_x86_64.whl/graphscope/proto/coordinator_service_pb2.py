# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: coordinator_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import message_pb2 as message__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x63oordinator_service.proto\x12\x06gs.rpc\x1a\rmessage.proto2\xba\x08\n\x12\x43oordinatorService\x12O\n\x0e\x43onnectSession\x12\x1d.gs.rpc.ConnectSessionRequest\x1a\x1e.gs.rpc.ConnectSessionResponse\x12@\n\tHeartBeat\x12\x18.gs.rpc.HeartBeatRequest\x1a\x19.gs.rpc.HeartBeatResponse\x12>\n\x07RunStep\x12\x16.gs.rpc.RunStepRequest\x1a\x17.gs.rpc.RunStepResponse(\x01\x30\x01\x12\x42\n\tFetchLogs\x12\x18.gs.rpc.FetchLogsRequest\x1a\x19.gs.rpc.FetchLogsResponse0\x01\x12I\n\x0c\x43loseSession\x12\x1b.gs.rpc.CloseSessionRequest\x1a\x1c.gs.rpc.CloseSessionResponse\x12\x37\n\x06\x41\x64\x64Lib\x12\x15.gs.rpc.AddLibRequest\x1a\x16.gs.rpc.AddLibResponse\x12m\n\x18\x43reateAnalyticalInstance\x12\'.gs.rpc.CreateAnalyticalInstanceRequest\x1a(.gs.rpc.CreateAnalyticalInstanceResponse\x12p\n\x19\x43reateInteractiveInstance\x12(.gs.rpc.CreateInteractiveInstanceRequest\x1a).gs.rpc.CreateInteractiveInstanceResponse\x12g\n\x16\x43reateLearningInstance\x12%.gs.rpc.CreateLearningInstanceRequest\x1a&.gs.rpc.CreateLearningInstanceResponse\x12j\n\x17\x43loseAnalyticalInstance\x12&.gs.rpc.CloseAnalyticalInstanceRequest\x1a\'.gs.rpc.CloseAnalyticalInstanceResponse\x12m\n\x18\x43loseInteractiveInstance\x12\'.gs.rpc.CloseInteractiveInstanceRequest\x1a(.gs.rpc.CloseInteractiveInstanceResponse\x12\x64\n\x15\x43loseLearningInstance\x12$.gs.rpc.CloseLearningInstanceRequest\x1a%.gs.rpc.CloseLearningInstanceResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'coordinator_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COORDINATORSERVICE']._serialized_start=53
  _globals['_COORDINATORSERVICE']._serialized_end=1135
# @@protoc_insertion_point(module_scope)
