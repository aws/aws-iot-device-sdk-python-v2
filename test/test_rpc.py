import test.echotestrpc.model as model
import test.echotestrpc.client as client
from awsiot.eventstreamrpc import (Connection, Header, LifecycleHandler, MessageAmendment)
from awscrt.io import (ClientBootstrap, DefaultHostResolver, EventLoopGroup)
from concurrent.futures import Future
from datetime import datetime, timezone
import logging
import os
from queue import Queue
from unittest import skipUnless, TestCase

import awsiot.greengrasscoreipc.client

TIMEOUT = 10

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] [%(name)s] - %(message)s')

EVENTSTREAM_ECHO_TEST = os.getenv('EVENTSTREAM_ECHO_TEST')


class StreamHandler(client.EchoStreamMessagesStreamHandler):
    def __init__(self):
        super().__init__()
        self.events = Queue()
        self.errors = Queue()
        self.closed = Future()
        self.error_callback_return_val = True
        # set this before activating operation
        self.operation = None
        # if something happens out of order, this gets set
        self.freakout = None

    def on_stream_event(self, event: model.EchoStreamingMessage) -> None:
        if not self.operation.get_response().done():
            self.freakout = "received event before initial response"
        if self.closed.done():
            self.freakout = "received event after close"
        self.events.put(event)

    def on_stream_error(self, error: Exception) -> bool:
        if not self.operation.get_response().done():
            self.freakout = "received event before initial response"
        if self.closed.done():
            self.freakout = "received event after close"
        self.errors.put(error)
        return self.error_callback_return_val

    def on_stream_closed(self) -> None:
        if self.closed.done():
            self.freakout = "received closed event twice"
        self.closed.set_result(None)


def connect_amender():
    headers = [Header.from_string('client-name', 'accepted.testy_mc_testerson')]
    return MessageAmendment(headers=headers)


@skipUnless(EVENTSTREAM_ECHO_TEST, "Skipping until we have permanent echo server")
class RpcTest(TestCase):
    def _connect(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        self.connection = Connection(
            host_name='127.0.0.1',
            port=8033,
            bootstrap=bootstrap,
            connect_message_amender=connect_amender)
        self.lifecycle_handler = LifecycleHandler()
        print("connecting...")
        connect_future = self.connection.connect(self.lifecycle_handler)
        connect_future.result(TIMEOUT)
        print("connected")

        self.echo_client = client.EchoTestRPCClient(self.connection)

    def test_echo_message(self):
        self._connect()

        operation = self.echo_client.new_echo_message()

        request = model.EchoMessageRequest(message=model.MessageData())
        request.message.string_message = '👁👄👁'
        request.message.boolean_message = True
        # hand-picked timestamp shouldn't lose precision when serialized to
        # json as floating point. also setting timezone to UTC because
        # response timezone will always be UTC
        request.message.time_message = datetime.fromtimestamp(946684800, tz=timezone.utc)
        request.message.document_message = {
            'inty': 4,
            'floaty': 4.0,
            'listy': [1, "two", 3.0, False, True, {}, None],
            'dicty': {'a': [1, 2, 3, {'e': 9}], 'b': None},
            'stringy': "qwer",
            'booly_t': True,
            'booly_f': False,
            'nully': None,
        }
        request.message.enum_message = model.FruitEnum.BANANA
        request.message.blob_message = bytes(list(range(256)))
        request.message.string_list_message = ['one', 'two', 'three']
        request.message.key_value_pair_list = [
            model.Pair(key='key1', value='value1'),
            model.Pair(key='key1', value='value1')]

        request_flush = operation.activate(request)
        self.assertIsNone(request_flush.result(TIMEOUT))

        response = operation.get_response().result(TIMEOUT)
        print("RESULT:", response)
        self.assertIsInstance(response, model.EchoMessageResponse)
        self.assertIsInstance(response.message, model.MessageData)
        # explicit tests for each member so it's clear exactly what went wrong
        self.assertEqual(request.message.string_message, response.message.string_message)
        self.assertEqual(request.message.boolean_message, response.message.boolean_message)
        self.assertEqual(request.message.document_message, response.message.document_message)
        self.assertEqual(request.message.enum_message, response.message.enum_message)
        self.assertEqual(request.message.blob_message, response.message.blob_message)
        self.assertEqual(request.message.string_list_message, response.message.string_list_message)
        self.assertEqual(request.message.key_value_pair_list, response.message.key_value_pair_list)
        self.assertIsInstance(response.message.time_message, datetime)
        self.assertAlmostEqual(request.message.time_message.timestamp(), response.message.time_message.timestamp())

        # ok now compare a whole class
        # if this fails, it's likely due to the datetime losing precision
        # and timezone info due to datetime->timestamp->datetime conversion
        self.assertEqual(request.message, response.message)

    def test_echo_streaming_message(self):
        self._connect()

        handler = StreamHandler()
        operation = self.echo_client.new_echo_stream_messages(handler)
        handler.operation = operation

        # send initial request
        flush = operation.activate(model.EchoStreamingRequest())
        flush.result(TIMEOUT)

        # send streaming request
        request_event = model.EchoStreamingMessage(key_value_pair=model.Pair(key='Kiki', value='Valerie'))
        flush = operation.send_stream_event(request_event)
        flush.result(TIMEOUT)

        # recv streaming response
        response_event = handler.events.get(timeout=TIMEOUT)
        self.assertEqual(request_event, response_event)

        # make sure nothing went wrong that we didn't expect to go wrong
        self.assertTrue(handler.errors.empty())
        self.assertIsNone(handler.freakout)
