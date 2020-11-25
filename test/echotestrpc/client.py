# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
import awsiot.eventstreamrpc as rpc
import concurrent.futures


class GetAllProductsOperation(model._GetAllProductsOperation):
    """
    GetAllProductsOperation

    Create with EchoTestRPCClient.new_get_all_products()
    """

    def activate(self, request: model.GetAllProductsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetAllProductsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetAllProductsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class CauseServiceErrorOperation(model._CauseServiceErrorOperation):
    """
    CauseServiceErrorOperation

    Create with EchoTestRPCClient.new_cause_service_error()
    """

    def activate(self, request: model.CauseServiceErrorRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial CauseServiceErrorRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of CauseServiceErrorResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class CauseStreamServiceToErrorStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for CauseStreamServiceToErrorOperation

    Inherit from this class and override methods to handle
    stream events during a CauseStreamServiceToErrorOperation.
    """

    def on_stream_event(self, event: model.EchoStreamingMessage) -> None:
        """
        Invoked when a EchoStreamingMessage is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class CauseStreamServiceToErrorOperation(model._CauseStreamServiceToErrorOperation):
    """
    CauseStreamServiceToErrorOperation

    Create with EchoTestRPCClient.new_cause_stream_service_to_error()
    """

    def activate(self, request: model.EchoStreamingRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial EchoStreamingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def send_stream_event(self, event: model.EchoStreamingMessage) -> concurrent.futures.Future:
        """
        Send next EchoStreamingMessage stream event.

        activate() must be called before send_stream_event().

        Returns a Future which completes with a result of None if the
        event is successfully written to the wire, or an exception if
        the event fails to send.
        """
        return self._send_stream_event(event)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of EchoStreamingResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class EchoStreamMessagesStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for EchoStreamMessagesOperation

    Inherit from this class and override methods to handle
    stream events during a EchoStreamMessagesOperation.
    """

    def on_stream_event(self, event: model.EchoStreamingMessage) -> None:
        """
        Invoked when a EchoStreamingMessage is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class EchoStreamMessagesOperation(model._EchoStreamMessagesOperation):
    """
    EchoStreamMessagesOperation

    Create with EchoTestRPCClient.new_echo_stream_messages()
    """

    def activate(self, request: model.EchoStreamingRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial EchoStreamingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def send_stream_event(self, event: model.EchoStreamingMessage) -> concurrent.futures.Future:
        """
        Send next EchoStreamingMessage stream event.

        activate() must be called before send_stream_event().

        Returns a Future which completes with a result of None if the
        event is successfully written to the wire, or an exception if
        the event fails to send.
        """
        return self._send_stream_event(event)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of EchoStreamingResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class EchoMessageOperation(model._EchoMessageOperation):
    """
    EchoMessageOperation

    Create with EchoTestRPCClient.new_echo_message()
    """

    def activate(self, request: model.EchoMessageRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial EchoMessageRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of EchoMessageResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetAllCustomersOperation(model._GetAllCustomersOperation):
    """
    GetAllCustomersOperation

    Create with EchoTestRPCClient.new_get_all_customers()
    """

    def activate(self, request: model.GetAllCustomersRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetAllCustomersRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetAllCustomersResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class EchoTestRPCClient(rpc.Client):
    """
    Client for the EchoTestRPC service.

    Args:
        connection: Connection that this client will use.
    """

    def __init__(self, connection: rpc.Connection):
        super().__init__(connection, model.SHAPE_INDEX)

    def new_get_all_products(self) -> GetAllProductsOperation:
        """
        Create a new GetAllProductsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetAllProductsOperation)

    def new_cause_service_error(self) -> CauseServiceErrorOperation:
        """
        Create a new CauseServiceErrorOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CauseServiceErrorOperation)

    def new_cause_stream_service_to_error(self, stream_handler: CauseStreamServiceToErrorStreamHandler) -> CauseStreamServiceToErrorOperation:
        """
        Create a new CauseStreamServiceToErrorOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(CauseStreamServiceToErrorOperation, stream_handler)

    def new_echo_stream_messages(self, stream_handler: EchoStreamMessagesStreamHandler) -> EchoStreamMessagesOperation:
        """
        Create a new EchoStreamMessagesOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(EchoStreamMessagesOperation, stream_handler)

    def new_echo_message(self) -> EchoMessageOperation:
        """
        Create a new EchoMessageOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(EchoMessageOperation)

    def new_get_all_customers(self) -> GetAllCustomersOperation:
        """
        Create a new GetAllCustomersOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetAllCustomersOperation)
