import concurrent.futures
import threading
from unittest import TestCase
from unittest.mock import patch
import io
import contextlib

from awsiot.greengrasscoreipc.client import SubscribeToTopicStreamHandler
from awsiot.greengrasscoreipc.model import CreateLocalDeploymentResponse, SubscribeToTopicResponse, \
    SubscriptionResponseMessage, BinaryMessage

TIMEOUT = 10.0 # seconds


class GGV2Test(TestCase):

    def _mock_operation(self, mock_op, response):
        activate_fut = concurrent.futures.Future()
        activate_fut.set_result(None)
        mock_op.activate.return_value = activate_fut
        response_fut = concurrent.futures.Future()
        response_fut.set_result(response)
        mock_op.get_response.return_value = response_fut
        return mock_op

    @patch('awsiot.greengrasscoreipc.client.GreengrassCoreIPCClient')
    @patch('awsiot.greengrasscoreipc.client.CreateLocalDeploymentOperation')
    @patch('awsiot.greengrasscoreipc.client.SubscribeToTopicOperation')
    def test_connect(self, mock_client, mock_deployment_op, mock_subscribe_op):
        from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2 as Client
        c = Client(client=mock_client)

        self._mock_operation(mock_deployment_op, CreateLocalDeploymentResponse(deployment_id="deployment"))
        mock_client.new_create_local_deployment.return_value = mock_deployment_op
        resp = c.create_local_deployment()
        self.assertEqual("deployment", resp.deployment_id)

        # Verify subscription works and callback is called on the executor thread
        self._mock_operation(mock_subscribe_op, SubscribeToTopicResponse(topic_name="abc"))
        mock_client.new_subscribe_to_topic.return_value = mock_subscribe_op

        subscription_fut = concurrent.futures.Future()
        thread_id_fut = concurrent.futures.Future()

        def on_stream_event(r):
            subscription_fut.set_result(r)
            thread_id_fut.set_result(threading.get_ident())
        resp, op = c.subscribe_to_topic(topic="abc", on_stream_event=on_stream_event)
        self.assertEqual("abc", resp.topic_name)

        sub_handler = mock_client.new_subscribe_to_topic.call_args[0][0]
        sub_handler.on_stream_event(SubscriptionResponseMessage(binary_message=BinaryMessage(message="xyz")))

        self.assertEqual("xyz".encode("utf-8"), subscription_fut.result(TIMEOUT).binary_message.message)
        self.assertNotEqual(threading.get_ident(), thread_id_fut.result(TIMEOUT))

        # Verify that when using the stream_handler option, the callback is run in the executor

        subscription_fut = concurrent.futures.Future()
        thread_id_fut = concurrent.futures.Future()

        class handler(SubscribeToTopicStreamHandler):
            def on_stream_event(self, event):
                on_stream_event(event)
        resp, op = c.subscribe_to_topic(topic="abc", stream_handler=handler())
        self.assertEqual("abc", resp.topic_name)

        sub_handler = mock_client.new_subscribe_to_topic.call_args[0][0]
        sub_handler.on_stream_event(SubscriptionResponseMessage(binary_message=BinaryMessage(message="xyz")))

        self.assertEqual("xyz".encode("utf-8"), subscription_fut.result(TIMEOUT).binary_message.message)
        self.assertNotEqual(threading.get_ident(), thread_id_fut.result(TIMEOUT))

        # Remove executor from client to verify that we are not running the callback in a different thread
        c = Client(client=mock_client, executor=None)

        subscription_fut = concurrent.futures.Future()
        thread_id_fut = concurrent.futures.Future()

        resp, op = c.subscribe_to_topic(topic="abc", on_stream_event=on_stream_event)
        self.assertEqual("abc", resp.topic_name)

        sub_handler = mock_client.new_subscribe_to_topic.call_args[0][0]
        sub_handler.on_stream_event(SubscriptionResponseMessage(binary_message=BinaryMessage(message="xyz")))

        self.assertEqual("xyz".encode("utf-8"), subscription_fut.result(TIMEOUT).binary_message.message)
        self.assertEqual(threading.get_ident(), thread_id_fut.result(TIMEOUT))

        # Verify we nicely print errors in user-provided handler methods
        def on_stream_event(r):
            raise ValueError("Broken!")

        c.subscribe_to_topic(topic="abc", on_stream_event=on_stream_event)
        sub_handler = mock_client.new_subscribe_to_topic.call_args[0][0]
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertRaises(ValueError, lambda: sub_handler.on_stream_event(
                SubscriptionResponseMessage(binary_message=BinaryMessage(message="xyz"))))
        self.assertIn("ValueError: Broken!", f.getvalue())
