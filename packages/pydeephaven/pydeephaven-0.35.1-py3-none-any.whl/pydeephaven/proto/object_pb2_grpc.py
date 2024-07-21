# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from pydeephaven.proto import object_pb2 as deephaven_dot_proto_dot_object__pb2

GRPC_GENERATED_VERSION = '1.63.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in deephaven/proto/object_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ObjectServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FetchObject = channel.unary_unary(
                '/io.deephaven.proto.backplane.grpc.ObjectService/FetchObject',
                request_serializer=deephaven_dot_proto_dot_object__pb2.FetchObjectRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_object__pb2.FetchObjectResponse.FromString,
                _registered_method=True)
        self.MessageStream = channel.stream_stream(
                '/io.deephaven.proto.backplane.grpc.ObjectService/MessageStream',
                request_serializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_object__pb2.StreamResponse.FromString,
                _registered_method=True)
        self.OpenMessageStream = channel.unary_stream(
                '/io.deephaven.proto.backplane.grpc.ObjectService/OpenMessageStream',
                request_serializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_object__pb2.StreamResponse.FromString,
                _registered_method=True)
        self.NextMessageStream = channel.unary_unary(
                '/io.deephaven.proto.backplane.grpc.ObjectService/NextMessageStream',
                request_serializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_object__pb2.BrowserNextResponse.FromString,
                _registered_method=True)


class ObjectServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FetchObject(self, request, context):
        """
        Fetches a server-side object as a binary payload and assorted other tickets pointing at
        other server-side objects that may need to be read to properly use this payload. The binary
        format is implementation specific, but the implementation should be specified by the "type"
        identifier in the typed ticket.

        Deprecated in favor of MessageStream, which is able to handle the same content.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MessageStream(self, request_iterator, context):
        """
        Provides a generic stream feature for Deephaven instances to use to add arbitrary functionality.
        Presently these take the form of "object type plugins", where server-side code can specify how
        an object could be serialized and/or communicate with a client. This gRPC stream is somewhat lower level
        than the plugin API, giving the server and client APIs features to correctly establish and
        control the stream. At this time, this is limited to a "ConnectRequest" to start the call.

        The first message sent to the server is expected to have a ConnectRequest, indicating which
        export ticket to connect to. It is an error for the client to attempt to connect to an object
        that has no plugin for its object type installed.

        The first request sent by the client should be a ConnectRequest. No other client message should
        be sent until the server responds. The server will respond with Data as soon as it is able (i.e.
        once the object in question has been resolved and the plugin has responded), indicating that the
        request was successful. After that point, the client may send Data requests.

        All replies from the server to the client contain Data instances. When sent from the server to
        the client, Data contains a bytes payload created by the server implementation of the plugin,
        and server-created export tickets containing any object references specified to be sent by the
        server-side plugin. As server-created exports, they are already resolved, and can be fetched or
        otherwise referenced right away. The client API is expected to wrap those tickets in appropriate
        objects, and the client is expected to release those tickets as appropriate, according to the
        plugin's use case. Note that it is possible for the "type" field to be null, indicating that
        there is no corresponding ObjectType plugin for these exported objects. This limits the client
        to specifying those tickets in a subsequent request, or releasing the ticket to let the object
        be garbage collected on the server.

        All Data instances sent from the client likewise contain a bytes payload, and may contain
        references to objects that already exist or may soon exist on the server, not just tickets sent
        by this same plugin. Note however that if those tickets are not yet resolved, neither the current
        Data nor subsequent requests can be processed by the plugin, as the required references can't be
        resolved.

        Presently there is no explicit "close" message to send, but plugin implementations can devise
        their own "half-close" protocol if they so choose. For now, if one end closes the connection,
        the other is expected to follow suit by closing their end too. At present, if there is an error
        with the stream, it is conveyed to the client in the usual gRPC fashion, but the server plugin
        will only be informed that the stream closed.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OpenMessageStream(self, request, context):
        """
        Half of the browser-based (browser's can't do bidirectional streams without websockets)
        implementation for MessageStream.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NextMessageStream(self, request, context):
        """
        Other half of the browser-based implementation for MessageStream.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ObjectServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FetchObject': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchObject,
                    request_deserializer=deephaven_dot_proto_dot_object__pb2.FetchObjectRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_object__pb2.FetchObjectResponse.SerializeToString,
            ),
            'MessageStream': grpc.stream_stream_rpc_method_handler(
                    servicer.MessageStream,
                    request_deserializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_object__pb2.StreamResponse.SerializeToString,
            ),
            'OpenMessageStream': grpc.unary_stream_rpc_method_handler(
                    servicer.OpenMessageStream,
                    request_deserializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_object__pb2.StreamResponse.SerializeToString,
            ),
            'NextMessageStream': grpc.unary_unary_rpc_method_handler(
                    servicer.NextMessageStream,
                    request_deserializer=deephaven_dot_proto_dot_object__pb2.StreamRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_object__pb2.BrowserNextResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'io.deephaven.proto.backplane.grpc.ObjectService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ObjectService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FetchObject(request,
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
            '/io.deephaven.proto.backplane.grpc.ObjectService/FetchObject',
            deephaven_dot_proto_dot_object__pb2.FetchObjectRequest.SerializeToString,
            deephaven_dot_proto_dot_object__pb2.FetchObjectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MessageStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/io.deephaven.proto.backplane.grpc.ObjectService/MessageStream',
            deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
            deephaven_dot_proto_dot_object__pb2.StreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def OpenMessageStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/io.deephaven.proto.backplane.grpc.ObjectService/OpenMessageStream',
            deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
            deephaven_dot_proto_dot_object__pb2.StreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def NextMessageStream(request,
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
            '/io.deephaven.proto.backplane.grpc.ObjectService/NextMessageStream',
            deephaven_dot_proto_dot_object__pb2.StreamRequest.SerializeToString,
            deephaven_dot_proto_dot_object__pb2.BrowserNextResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
