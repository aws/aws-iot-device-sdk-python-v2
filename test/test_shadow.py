# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import io, mqtt, mqtt5, mqtt_request_response
from awscrt.mqtt_request_response import SubscriptionStatusEvent, SubscriptionStatusEventType

import awsiot
from awsiot import iotshadow

from concurrent.futures import Future
import os
import unittest
import uuid

TIMEOUT = 30.0


def create_client_id():
    return f"aws-iot-device-sdk-python-v2-shadow-test-{uuid.uuid4()}"


def _get_env_variable(env_name):
    env_data = os.environ.get(env_name)
    if not env_data:
        raise unittest.SkipTest(f"test requires env var: {env_name}")
    return env_data


class ShadowTestCallbacks():
    def __init__(self):
        self.future_connection_success = Future()
        self.future_stopped = Future()

    def ws_handshake_transform(self, transform_args):
        transform_args.set_done()

    def on_publish_received(self, publish_received_data: mqtt5.PublishReceivedData):
        pass

    def on_lifecycle_stopped(self, lifecycle_stopped: mqtt5.LifecycleStoppedData):
        if self.future_stopped:
            self.future_stopped.set_result(None)

    def on_lifecycle_attempting_connect(self, lifecycle_attempting_connect: mqtt5.LifecycleAttemptingConnectData):
        pass

    def on_lifecycle_connection_success(self, lifecycle_connection_success: mqtt5.LifecycleConnectSuccessData):
        if self.future_connection_success:
            self.future_connection_success.set_result(lifecycle_connection_success)

    def on_lifecycle_connection_failure(self, lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
        if self.future_connection_success:
            if self.future_connection_success.done():
                pass
            else:
                self.future_connection_success.set_exception(lifecycle_connection_failure.exception)

    def on_lifecycle_disconnection(self, lifecycle_disconnect_data: mqtt5.LifecycleDisconnectData):
        pass


class ShadowServiceTest(unittest.TestCase):

    def _create_protocol_client5(self):

        input_host_name = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_HOST")
        input_cert = _get_env_variable("AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_MQTT5_IOT_KEY_PATH")

        client_options = mqtt5.ClientOptions(
            host_name=input_host_name,
            port=8883
        )

        tls_ctx_options = io.TlsContextOptions.create_client_with_mtls_from_path(
            input_cert,
            input_key
        )
        client_options.tls_ctx = io.ClientTlsContext(tls_ctx_options)

        client_options.connect_options = mqtt5.ConnectPacket()
        client_options.connect_options.client_id = create_client_id()

        callbacks = ShadowTestCallbacks()
        client_options.on_lifecycle_event_stopped_fn = callbacks.on_lifecycle_stopped
        client_options.on_lifecycle_event_connection_success_fn = callbacks.on_lifecycle_connection_success
        client_options.on_lifecycle_event_connection_failure_fn = callbacks.on_lifecycle_connection_failure
        client_options.on_lifecycle_event_stopped_fn = callbacks.on_lifecycle_stopped

        protocol_client = mqtt5.Client(client_options)
        protocol_client.start()

        callbacks.future_connection_success.result(TIMEOUT)

        return protocol_client, callbacks

    def _shutdown_protocol_client5(self, protocol_client, callbacks):

        protocol_client.stop()
        callbacks.future_stopped.result(TIMEOUT)

    def _create_protocol_client311(self):

        input_host_name = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_HOST")
        input_cert = _get_env_variable("AWS_TEST_MQTT5_IOT_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_MQTT5_IOT_KEY_PATH")

        tls_ctx_options = io.TlsContextOptions.create_client_with_mtls_from_path(
            input_cert,
            input_key
        )
        tls_ctx = io.ClientTlsContext(tls_ctx_options)

        client = mqtt.Client(None, tls_ctx)

        protocol_client = mqtt.Connection(
            client=client,
            client_id=create_client_id(),
            host_name=input_host_name,
            port=8883,
            ping_timeout_ms=10000,
            keep_alive_secs=30
        )
        protocol_client.connect().result(TIMEOUT)

        return protocol_client

    def _shutdown_protocol_client311(self, protocol_client):
        protocol_client.disconnect().result(TIMEOUT)

    def _create_shadow_client(
            self,
            protocol_client,
            max_request_response_subscriptions,
            max_streaming_subscriptions,
            operation_timeout_seconds):
        rr_client_options = mqtt_request_response.ClientOptions(
            max_request_response_subscriptions, max_streaming_subscriptions)
        rr_client_options.operation_timeout_in_seconds = operation_timeout_seconds

        shadow_client = iotshadow.IotShadowClientV2(protocol_client, rr_client_options)

        return shadow_client

    def _do_shadow_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()

        test_callable(protocol_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_shadow_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()

        test_callable(protocol_client)

        self._shutdown_protocol_client311(protocol_client)

    def _do_shadow_operation_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()
        shadow_client = self._create_shadow_client(protocol_client, 2, 2, 30)

        test_callable(shadow_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_shadow_operation_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()
        shadow_client = self._create_shadow_client(protocol_client, 2, 2, 30)

        test_callable(shadow_client)

        self._shutdown_protocol_client311(protocol_client)

    def _get_non_existent_named_shadow(self, shadow_client, thing_name, shadow_name):
        try:
            shadow_client.get_named_shadow(iotshadow.GetNamedShadowRequest(
                thing_name=thing_name,
                shadow_name=shadow_name,
            )).result(TIMEOUT)
            self.assertTrue(False)
        except Exception as e:
            assert isinstance(e, awsiot.V2ServiceException)
            assert isinstance(e.modeled_error, iotshadow.V2ErrorResponse)
            self.assertEqual(404, e.modeled_error.code)
            self.assertIn("No shadow exists with name", e.modeled_error.message)

    def _do_get_non_existent_named_shadow_test(self, shadow_client):
        self._get_non_existent_named_shadow(shadow_client, uuid.uuid4(), uuid.uuid4())

    def _create_named_shadow(self, shadow_client, thing_name, shadow_name, state_document):
        request = iotshadow.UpdateNamedShadowRequest(
            thing_name=thing_name,
            shadow_name=shadow_name,
            state=iotshadow.ShadowState(
                desired=state_document,
                reported=state_document,
            )
        )

        response = shadow_client.update_named_shadow(request).result(TIMEOUT)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.state)
        self.assertEqual(response.state.desired, state_document)
        self.assertEqual(response.state.reported, state_document)

    def _get_named_shadow(self, shadow_client, thing_name, shadow_name, expected_state_document):
        request = iotshadow.GetNamedShadowRequest(
            thing_name=thing_name,
            shadow_name=shadow_name,
        )

        response = shadow_client.get_named_shadow(request).result(TIMEOUT)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.state)
        self.assertEqual(response.state.desired, expected_state_document)
        self.assertEqual(response.state.reported, expected_state_document)

    def _delete_named_shadow(self, shadow_client, thing_name, shadow_name):
        request = iotshadow.DeleteNamedShadowRequest(
            thing_name=thing_name,
            shadow_name=shadow_name,
        )

        response = shadow_client.delete_named_shadow(request).result(TIMEOUT)
        self.assertIsNotNone(response)

    def _do_create_get_delete_shadow_test(self, shadow_client):
        thing_name = uuid.uuid4()
        shadow_name = uuid.uuid4()
        document = {
            "Color": "Green",
            "On": True
        }

        self._get_non_existent_named_shadow(shadow_client, thing_name, shadow_name)

        try:
            self._create_named_shadow(shadow_client, thing_name, shadow_name, document)
            self._get_named_shadow(shadow_client, thing_name, shadow_name, document)
        finally:
            self._delete_named_shadow(shadow_client, thing_name, shadow_name)

        self._get_non_existent_named_shadow(shadow_client, thing_name, shadow_name)

    def _update_named_shadow_desired(self, shadow_client, thing_name, shadow_name, state_document):
        request = iotshadow.UpdateNamedShadowRequest(
            thing_name=thing_name,
            shadow_name=shadow_name,
            state=iotshadow.ShadowState(
                desired=state_document,
            )
        )

        response = shadow_client.update_named_shadow(request).result(TIMEOUT)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.state)
        self.assertEqual(response.state.desired, state_document)

    def _do_update_shadow_test(self, shadow_client):
        thing_name = uuid.uuid4()
        shadow_name = uuid.uuid4()
        document = {
            "Color": "Green",
            "On": True
        }

        self._get_non_existent_named_shadow(shadow_client, thing_name, shadow_name)

        try:
            self._create_named_shadow(shadow_client, thing_name, shadow_name, document)

            delta_subscription_future = Future()
            delta_future = Future()

            def on_delta_subscription_event(event : SubscriptionStatusEvent):
                if event.type == SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED:
                    delta_subscription_future.set_result(event)

            delta_event_stream = shadow_client.create_named_shadow_delta_updated_stream(
                iotshadow.NamedShadowDeltaUpdatedSubscriptionRequest(
                    thing_name=thing_name,
                    shadow_name=shadow_name,
                ),
                awsiot.ServiceStreamOptions(
                    subscription_status_listener=on_delta_subscription_event,
                    incoming_event_listener=lambda event: delta_future.set_result(event),
                )
            )

            delta_event_stream.open()
            delta_subscription_event = delta_subscription_future.result(TIMEOUT)

            self.assertEqual(mqtt_request_response.SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED,
                             delta_subscription_event.type)

            update_subscription_future = Future()
            update_future = Future()

            def on_updated_subscription_event(event : SubscriptionStatusEvent):
                if event.type == SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED:
                    update_subscription_future.set_result(event)

            update_event_stream = shadow_client.create_named_shadow_updated_stream(
                iotshadow.NamedShadowUpdatedSubscriptionRequest(
                    thing_name=thing_name,
                    shadow_name=shadow_name,
                ),
                awsiot.ServiceStreamOptions(
                    subscription_status_listener=on_updated_subscription_event,
                    incoming_event_listener=lambda event: update_future.set_result(event),
                )
            )

            update_event_stream.open()
            update_subscription_event = update_subscription_future.result(TIMEOUT)

            self.assertEqual(mqtt_request_response.SubscriptionStatusEventType.SUBSCRIPTION_ESTABLISHED,
                             update_subscription_event.type)

            new_document = {
                "Color": "Red",
                "On": False
            }
            self._update_named_shadow_desired(shadow_client, thing_name, shadow_name, new_document)

            delta_event = delta_future.result(TIMEOUT)
            self.assertEqual(new_document, delta_event.state)

            update_event = update_future.result(TIMEOUT)
            self.assertEqual(new_document, update_event.current.state.desired)

        finally:
            self._delete_named_shadow(shadow_client, thing_name, shadow_name)

        self._get_non_existent_named_shadow(shadow_client, thing_name, shadow_name)

    # ==============================================================
    #             CREATION SUCCESS TEST CASES
    # ==============================================================

    def test_client_creation_success5(self):
        self._do_shadow_test5(lambda protocol_client: self._create_shadow_client(protocol_client, 2, 2, 30))

    def test_client_creation_success311(self):
        self._do_shadow_test311(lambda protocol_client: self._create_shadow_client(protocol_client, 2, 2, 30))

    # ==============================================================
    #             CREATION FAILURE TEST CASES
    # ==============================================================

    def test_client_creation_failure_no_protocol_client(self):
        self.assertRaises(Exception, self._create_shadow_client, None, 2, 2, 30)

    # ==============================================================
    #             REQUEST RESPONSE OPERATION TEST CASES
    # ==============================================================
    def test_get_non_existent_named_shadow5(self):
        self._do_shadow_operation_test5(lambda shadow_client: self._do_get_non_existent_named_shadow_test(shadow_client))

    def test_get_non_existent_named_shadow311(self):
        self._do_shadow_operation_test311(lambda shadow_client: self._do_get_non_existent_named_shadow_test(shadow_client))

    def test_create_get_delete_shadow5(self):
        self._do_shadow_operation_test5(lambda shadow_client: self._do_create_get_delete_shadow_test(shadow_client))

    def test_create_get_delete_shadow311(self):
        self._do_shadow_operation_test311(lambda shadow_client: self._do_create_get_delete_shadow_test(shadow_client))

    def test_update_shadow5(self):
        self._do_shadow_operation_test5(lambda shadow_client: self._do_update_shadow_test(shadow_client))

    def test_update_shadow311(self):
        self._do_shadow_operation_test311(lambda shadow_client: self._do_update_shadow_test(shadow_client))


if __name__ == 'main':
    unittest.main()
