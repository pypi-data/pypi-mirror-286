# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from groot.sdk import client_ddl_service_pb2 as groot_dot_sdk_dot_client__ddl__service__pb2

GRPC_GENERATED_VERSION = '1.65.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.66.0'
SCHEDULED_RELEASE_DATE = 'August 6, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in groot/sdk/client_ddl_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ClientDdlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.submitDdl = channel.unary_unary(
                '/gs.rpc.groot.ClientDdl/submitDdl',
                request_serializer=groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlRequest.SerializeToString,
                response_deserializer=groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlResponse.FromString,
                _registered_method=True)


class ClientDdlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def submitDdl(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientDdlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'submitDdl': grpc.unary_unary_rpc_method_handler(
                    servicer.submitDdl,
                    request_deserializer=groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlRequest.FromString,
                    response_serializer=groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gs.rpc.groot.ClientDdl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gs.rpc.groot.ClientDdl', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ClientDdl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def submitDdl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gs.rpc.groot.ClientDdl/submitDdl',
            groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlRequest.SerializeToString,
            groot_dot_sdk_dot_client__ddl__service__pb2.SubmitDdlResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
