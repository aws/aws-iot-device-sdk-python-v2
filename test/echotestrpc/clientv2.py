# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
from .client import EchoTestRPCClient
from . import client

import concurrent.futures
import datetime
import typing


class EchoTestRPCClientV2:
    """
    V2 client for the EchoTestRPC service.

    Args:
        client: Connection that this client will use. If you do not provide one, it will be made automatically.
        executor: Executor used to run on_stream_event and on_stream_closed callbacks to avoid blocking the networking
         thread. By default, a ThreadPoolExecutor will be created and used. Use None to run callbacks in the
         networking thread, but understand that your code can deadlock the networking thread if it performs a
         synchronous network call.
    """

    def __init__(self, client: typing.Optional[EchoTestRPCClient] = None,
                 executor: typing.Optional[concurrent.futures.Executor] = True):
        if client is None:
            import awsiot.greengrasscoreipc
            client = awsiot.greengrasscoreipc.connect()
        self.client = client
        if executor is True:
            executor = concurrent.futures.ThreadPoolExecutor()
        self.executor = executor

    def close(self, *, executor_wait=True) -> concurrent.futures.Future:
        """
        Close the underlying connection and shutdown the event executor (if any)

        Args:
            executor_wait: If true (default), then this method will block until the executor finishes running
                all tasks and shuts down.

        Returns:
            The future which will complete
            when the shutdown process is done. The future will have an
            exception if shutdown was caused by an error, or a result
            of None if the shutdown was clean and user-initiated.
        """
        fut = self.client.close()
        if self.executor is not None:
            self.executor.shutdown(wait=executor_wait)
        return fut

    def __combine_futures(self, future1: concurrent.futures.Future,
                          future2: concurrent.futures.Future) -> concurrent.futures.Future:
        def callback(*args, **kwargs):
            try:
                future1.result()
            except Exception as e:
                future2.set_exception(e)
        future1.add_done_callback(callback)
        return future2

    @staticmethod
    def __handle_error():
        import sys
        import traceback
        traceback.print_exc(file=sys.stderr)

    def __wrap_error(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.__handle_error()
                raise e
        return wrapper

    def __create_stream_handler(real_self, operation, on_stream_event, on_stream_error, on_stream_closed):
        stream_handler_type = type(operation + 'Handler', (getattr(client, operation + "StreamHandler"),), {})
        if on_stream_event is not None:
            on_stream_event = real_self.__wrap_error(on_stream_event)
            def handler(self, event):
                if real_self.executor is not None:
                    real_self.executor.submit(on_stream_event, event)
                else:
                    on_stream_event(event)
            setattr(stream_handler_type, "on_stream_event", handler)
        if on_stream_error is not None:
            on_stream_error = real_self.__wrap_error(on_stream_error)
            def handler(self, error):
                return on_stream_error(error)
            setattr(stream_handler_type, "on_stream_error", handler)
        if on_stream_closed is not None:
            on_stream_closed = real_self.__wrap_error(on_stream_closed)
            def handler(self):
                if real_self.executor is not None:
                    real_self.executor.submit(on_stream_closed)
                else:
                    on_stream_closed()
            setattr(stream_handler_type, "on_stream_closed", handler)
        return stream_handler_type()

    def __handle_stream_handler(real_self, operation, stream_handler, on_stream_event, on_stream_error, on_stream_closed):
        if stream_handler is not None and (on_stream_event is not None or on_stream_error is not None or on_stream_closed is not None):
            raise ValueError("Must choose either stream_handler or on_stream_event/on_stream_error/on_stream_closed")
        if stream_handler is not None and real_self.executor is not None:
            return real_self.__create_stream_handler(operation, stream_handler.on_stream_event,
                                                     stream_handler.on_stream_error, stream_handler.on_stream_closed)
        if stream_handler is None:
            return real_self.__create_stream_handler(operation, on_stream_event, on_stream_error, on_stream_closed)
        return stream_handler

    def cause_service_error(self) -> model.CauseServiceErrorResponse:
        """
        Perform the CauseServiceError operation synchronously.

        """
        return self.cause_service_error_async().result()

    def cause_service_error_async(self):  # type: (...) -> concurrent.futures.Future[model.CauseServiceErrorResponse]
        """
        Perform the CauseServiceError operation asynchronously.

        """
        request = model.CauseServiceErrorRequest()
        operation = self.client.new_cause_service_error()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def cause_stream_service_to_error(self, *,
        stream_handler: typing.Optional[client.CauseStreamServiceToErrorStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.EchoStreamingMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.EchoStreamingResponse, client.CauseStreamServiceToErrorOperation]:
        """
        Perform the CauseStreamServiceToError operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.cause_stream_service_to_error_async(
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def cause_stream_service_to_error_async(self, *,
        stream_handler: client.CauseStreamServiceToErrorStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.EchoStreamingMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.EchoStreamingResponse], client.CauseStreamServiceToErrorOperation]
        """
        Perform the CauseStreamServiceToError operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("CauseStreamServiceToError", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.EchoStreamingRequest()
        operation = self.client.new_cause_stream_service_to_error(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def echo_message(self, *,
        message: typing.Optional[model.MessageData] = None) -> model.EchoMessageResponse:
        """
        Perform the EchoMessage operation synchronously.

        Args:
            message: 
        """
        return self.echo_message_async(message=message).result()

    def echo_message_async(self, *,
        message: typing.Optional[model.MessageData] = None):  # type: (...) -> concurrent.futures.Future[model.EchoMessageResponse]
        """
        Perform the EchoMessage operation asynchronously.

        Args:
            message: 
        """
        request = model.EchoMessageRequest(message=message)
        operation = self.client.new_echo_message()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def echo_stream_messages(self, *,
        stream_handler: typing.Optional[client.EchoStreamMessagesStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.EchoStreamingMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.EchoStreamingResponse, client.EchoStreamMessagesOperation]:
        """
        Perform the EchoStreamMessages operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.echo_stream_messages_async(
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def echo_stream_messages_async(self, *,
        stream_handler: client.EchoStreamMessagesStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.EchoStreamingMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.EchoStreamingResponse], client.EchoStreamMessagesOperation]
        """
        Perform the EchoStreamMessages operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("EchoStreamMessages", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.EchoStreamingRequest()
        operation = self.client.new_echo_stream_messages(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def get_all_customers(self) -> model.GetAllCustomersResponse:
        """
        Perform the GetAllCustomers operation synchronously.

        """
        return self.get_all_customers_async().result()

    def get_all_customers_async(self):  # type: (...) -> concurrent.futures.Future[model.GetAllCustomersResponse]
        """
        Perform the GetAllCustomers operation asynchronously.

        """
        request = model.GetAllCustomersRequest()
        operation = self.client.new_get_all_customers()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_all_products(self) -> model.GetAllProductsResponse:
        """
        Perform the GetAllProducts operation synchronously.

        """
        return self.get_all_products_async().result()

    def get_all_products_async(self):  # type: (...) -> concurrent.futures.Future[model.GetAllProductsResponse]
        """
        Perform the GetAllProducts operation asynchronously.

        """
        request = model.GetAllProductsRequest()
        operation = self.client.new_get_all_products()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())
