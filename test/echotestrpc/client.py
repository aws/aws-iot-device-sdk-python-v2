# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
import awsiot.eventstreamrpc as rpc
import concurrent.futures


class GetAllProductsOperation(model._GetAllProductsOperation):
    def activate(self, request: model.GetAllProductsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetAllProductsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetAllProductsResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class CauseServiceErrorOperation(model._CauseServiceErrorOperation):
    def activate(self, request: model.CauseServiceErrorRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.CauseServiceErrorRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.CauseServiceErrorResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class CauseStreamServiceToErrorStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.EchoStreamingMessage) -> None:
        """
        Invoked when a model.EchoStreamingMessage is received.
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
    def activate(self, request: model.EchoStreamingRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.EchoStreamingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def send_stream_event(self, event: model.EchoStreamingMessage) -> concurrent.futures.Future:
        """
        Send next stream event.

        activate() must be called before send_stream_event().

        Returns a Future which completes with a result of None if the
        event is successfully written to the wire, or an exception if
        the event fails to send.
        """
        return self._send_stream_event(event)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.EchoStreamingResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class EchoStreamMessagesStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.EchoStreamingMessage) -> None:
        """
        Invoked when a model.EchoStreamingMessage is received.
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
    def activate(self, request: model.EchoStreamingRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.EchoStreamingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def send_stream_event(self, event: model.EchoStreamingMessage) -> concurrent.futures.Future:
        """
        Send next stream event.

        activate() must be called before send_stream_event().

        Returns a Future which completes with a result of None if the
        event is successfully written to the wire, or an exception if
        the event fails to send.
        """
        return self._send_stream_event(event)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.EchoStreamingResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class EchoMessageOperation(model._EchoMessageOperation):
    def activate(self, request: model.EchoMessageRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.EchoMessageRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.EchoMessageResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GetAllCustomersOperation(model._GetAllCustomersOperation):
    def activate(self, request: model.GetAllCustomersRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetAllCustomersRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetAllCustomersResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class EchoTestRPCClient(rpc.Client):

    def __init__(self, connection: rpc.Connection):
        super().__init__(connection, model.SHAPE_INDEX)

    def new_get_all_products(self) -> GetAllProductsOperation:
        return self._new_operation(GetAllProductsOperation)

    def new_cause_service_error(self) -> CauseServiceErrorOperation:
        return self._new_operation(CauseServiceErrorOperation)

    def new_cause_stream_service_to_error(self, stream_handler: CauseStreamServiceToErrorStreamHandler) -> CauseStreamServiceToErrorOperation:
        return self._new_operation(CauseStreamServiceToErrorOperation, stream_handler)

    def new_echo_stream_messages(self, stream_handler: EchoStreamMessagesStreamHandler) -> EchoStreamMessagesOperation:
        return self._new_operation(EchoStreamMessagesOperation, stream_handler)

    def new_echo_message(self) -> EchoMessageOperation:
        return self._new_operation(EchoMessageOperation)

    def new_get_all_customers(self) -> GetAllCustomersOperation:
        return self._new_operation(GetAllCustomersOperation)
