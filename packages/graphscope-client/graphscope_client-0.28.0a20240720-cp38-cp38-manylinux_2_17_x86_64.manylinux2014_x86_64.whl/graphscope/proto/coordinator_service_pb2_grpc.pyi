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
import abc
import collections.abc
import grpc
import message_pb2

class CoordinatorServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    ConnectSession: grpc.UnaryUnaryMultiCallable[
        message_pb2.ConnectSessionRequest,
        message_pb2.ConnectSessionResponse,
    ]
    """Connect a session."""
    HeartBeat: grpc.UnaryUnaryMultiCallable[
        message_pb2.HeartBeatRequest,
        message_pb2.HeartBeatResponse,
    ]
    """Heart Beat between client and coordinator"""
    RunStep: grpc.StreamStreamMultiCallable[
        message_pb2.RunStepRequest,
        message_pb2.RunStepResponse,
    ]
    """Drives the graph computation."""
    FetchLogs: grpc.UnaryStreamMultiCallable[
        message_pb2.FetchLogsRequest,
        message_pb2.FetchLogsResponse,
    ]
    """Fetch analytical engine logs."""
    CloseSession: grpc.UnaryUnaryMultiCallable[
        message_pb2.CloseSessionRequest,
        message_pb2.CloseSessionResponse,
    ]
    """Closes a session."""
    AddLib: grpc.UnaryUnaryMultiCallable[
        message_pb2.AddLibRequest,
        message_pb2.AddLibResponse,
    ]
    """Distribute the specified library to servers"""
    CreateAnalyticalInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CreateAnalyticalInstanceRequest,
        message_pb2.CreateAnalyticalInstanceResponse,
    ]
    CreateInteractiveInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CreateInteractiveInstanceRequest,
        message_pb2.CreateInteractiveInstanceResponse,
    ]
    CreateLearningInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CreateLearningInstanceRequest,
        message_pb2.CreateLearningInstanceResponse,
    ]
    CloseAnalyticalInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CloseAnalyticalInstanceRequest,
        message_pb2.CloseAnalyticalInstanceResponse,
    ]
    CloseInteractiveInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CloseInteractiveInstanceRequest,
        message_pb2.CloseInteractiveInstanceResponse,
    ]
    CloseLearningInstance: grpc.UnaryUnaryMultiCallable[
        message_pb2.CloseLearningInstanceRequest,
        message_pb2.CloseLearningInstanceResponse,
    ]

class CoordinatorServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ConnectSession(
        self,
        request: message_pb2.ConnectSessionRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.ConnectSessionResponse:
        """Connect a session."""
    @abc.abstractmethod
    def HeartBeat(
        self,
        request: message_pb2.HeartBeatRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.HeartBeatResponse:
        """Heart Beat between client and coordinator"""
    @abc.abstractmethod
    def RunStep(
        self,
        request_iterator: collections.abc.Iterator[message_pb2.RunStepRequest],
        context: grpc.ServicerContext,
    ) -> collections.abc.Iterator[message_pb2.RunStepResponse]:
        """Drives the graph computation."""
    @abc.abstractmethod
    def FetchLogs(
        self,
        request: message_pb2.FetchLogsRequest,
        context: grpc.ServicerContext,
    ) -> collections.abc.Iterator[message_pb2.FetchLogsResponse]:
        """Fetch analytical engine logs."""
    @abc.abstractmethod
    def CloseSession(
        self,
        request: message_pb2.CloseSessionRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CloseSessionResponse:
        """Closes a session."""
    @abc.abstractmethod
    def AddLib(
        self,
        request: message_pb2.AddLibRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.AddLibResponse:
        """Distribute the specified library to servers"""
    @abc.abstractmethod
    def CreateAnalyticalInstance(
        self,
        request: message_pb2.CreateAnalyticalInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CreateAnalyticalInstanceResponse: ...
    @abc.abstractmethod
    def CreateInteractiveInstance(
        self,
        request: message_pb2.CreateInteractiveInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CreateInteractiveInstanceResponse: ...
    @abc.abstractmethod
    def CreateLearningInstance(
        self,
        request: message_pb2.CreateLearningInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CreateLearningInstanceResponse: ...
    @abc.abstractmethod
    def CloseAnalyticalInstance(
        self,
        request: message_pb2.CloseAnalyticalInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CloseAnalyticalInstanceResponse: ...
    @abc.abstractmethod
    def CloseInteractiveInstance(
        self,
        request: message_pb2.CloseInteractiveInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CloseInteractiveInstanceResponse: ...
    @abc.abstractmethod
    def CloseLearningInstance(
        self,
        request: message_pb2.CloseLearningInstanceRequest,
        context: grpc.ServicerContext,
    ) -> message_pb2.CloseLearningInstanceResponse: ...

def add_CoordinatorServiceServicer_to_server(servicer: CoordinatorServiceServicer, server: grpc.Server) -> None: ...
