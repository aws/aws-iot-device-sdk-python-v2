# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
import pdb

from awscrt import io, mqtt, mqtt5, mqtt_request_response
import awsiot
from awsiot import iotidentity

import boto3
from concurrent.futures import Future
import os
import time
import unittest
import uuid

TIMEOUT = 30.0


def create_client_id():
    return f"test-{uuid.uuid4().hex}"


def _get_env_variable(env_name):
    env_data = os.environ.get(env_name)
    if not env_data:
        raise unittest.SkipTest(f"test requires env var: {env_name}")
    return env_data


class IdentityTestCallbacks():
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

class TestContext():
    def __init__(self):
        self.region = _get_env_variable("AWS_TEST_MQTT5_IOT_CORE_REGION")
        self.csr_path = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_CSR_PATH")
        self.provisioning_template_name = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_TEMPLATE_NAME")
        self.thing_name = None
        self.certificate_id = None

class IdentityServiceTest(unittest.TestCase):

    def _create_protocol_client5(self):

        input_host_name = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_HOST")
        input_cert = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_KEY_PATH")

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

        callbacks = IdentityTestCallbacks()
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

        input_host_name = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_HOST")
        input_cert = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_CERTIFICATE_PATH")
        input_key = _get_env_variable("AWS_TEST_IOT_CORE_PROVISIONING_KEY_PATH")

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

    def _create_identity_client(
            self,
            protocol_client,
            max_request_response_subscriptions,
            max_streaming_subscriptions,
            operation_timeout_seconds):
        rr_client_options = mqtt_request_response.ClientOptions(
            max_request_response_subscriptions, max_streaming_subscriptions)
        rr_client_options.operation_timeout_in_seconds = operation_timeout_seconds

        identity_client = iotidentity.IotIdentityClientV2(protocol_client, rr_client_options)

        return identity_client

    def _do_identity_creation_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()

        test_callable(protocol_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_identity_creation_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()

        test_callable(protocol_client)

        self._shutdown_protocol_client311(protocol_client)

    def _do_identity_operation_test5(self, test_callable):
        (protocol_client, callbacks) = self._create_protocol_client5()
        identity_client = self._create_identity_client(protocol_client, 2, 2, 30)

        test_callable(identity_client)

        self._shutdown_protocol_client5(protocol_client, callbacks)

    def _do_identity_operation_test311(self, test_callable):
        protocol_client = self._create_protocol_client311()
        identity_client = self._create_identity_client(protocol_client, 2, 2, 30)

        test_callable(identity_client)

        self._shutdown_protocol_client311(protocol_client)

    def _tear_down(self, test_context):
        iot_client = boto3.client('iot',region_name=test_context.region)
        certificate_arn = None
        if test_context.certificate_id is not None:
            describe_response = iot_client.describe_certificate(certificateId=test_context.certificate_id)
            certificate_arn = describe_response['certificateDescription']['certificateArn']

        if test_context.thing_name is not None:
            if certificate_arn is not None:
                iot_client.detach_thing_principal(thingName=test_context.thing_name, principal=certificate_arn)
                time.sleep(1)

            iot_client.delete_thing(thingName=test_context.thing_name)
            time.sleep(1)

        if test_context.certificate_id is not None:
            iot_client.update_certificate(certificateId=test_context.certificate_id, newStatus='INACTIVE')

            list_policies_response = iot_client.list_attached_policies(target=certificate_arn)
            for policy in list_policies_response['policies']:
                iot_client.detach_policy(target=certificate_arn, policyName=policy['policyName'])

            time.sleep(1)
            iot_client.delete_certificate(certificateId=test_context.certificate_id)

    def _do_basic_provisioning_test(self, identity_client):
        test_context = TestContext()
        try:
            create_response = identity_client.create_keys_and_certificate(iotidentity.CreateKeysAndCertificateRequest()).result(TIMEOUT)
            test_context.certificate_id = create_response.certificate_id

            self.assertIsNotNone(create_response.certificate_id)
            self.assertIsNotNone(create_response.certificate_pem)
            self.assertIsNotNone(create_response.private_key)
            self.assertIsNotNone(create_response.certificate_ownership_token)

            register_thing_request = iotidentity.RegisterThingRequest(
                template_name=test_context.provisioning_template_name,
                certificate_ownership_token=create_response.certificate_ownership_token,
                parameters= {
                    "SerialNumber": uuid.uuid4().hex,
                }
            )

            register_thing_response = identity_client.register_thing(register_thing_request).result(TIMEOUT)
            test_context.thing_name = register_thing_response.thing_name;

            self.assertIsNotNone(register_thing_response.thing_name)
        finally:
            self._tear_down(test_context)

    def _do_csr_provisioning_test(self, identity_client):
        test_context = TestContext()
        try:
            with open(test_context.csr_path, "r") as csr_file:
                csr_data = csr_file.read()

            create_response = identity_client.create_certificate_from_csr(
                iotidentity.CreateCertificateFromCsrRequest(
                    certificate_signing_request=csr_data,
                )).result(TIMEOUT)

            test_context.certificate_id = create_response.certificate_id

            self.assertIsNotNone(create_response.certificate_id)
            self.assertIsNotNone(create_response.certificate_pem)
            self.assertIsNotNone(create_response.certificate_ownership_token)

            register_thing_request = iotidentity.RegisterThingRequest(
                template_name=test_context.provisioning_template_name,
                certificate_ownership_token=create_response.certificate_ownership_token,
                parameters= {
                    "SerialNumber": uuid.uuid4().hex,
                }
            )

            register_thing_response = identity_client.register_thing(register_thing_request).result(TIMEOUT)
            test_context.thing_name = register_thing_response.thing_name;

            self.assertIsNotNone(register_thing_response.thing_name)
        finally:
            self._tear_down(test_context)

    # ==============================================================
    #             CREATION SUCCESS TEST CASES
    # ==============================================================
    def test_client_creation_success5(self):
        self._do_identity_creation_test5(lambda protocol_client: self._create_identity_client(protocol_client, 2, 2, 30))

    def test_client_creation_success311(self):
        self._do_identity_creation_test311(lambda protocol_client: self._create_identity_client(protocol_client, 2, 2, 30))

    # ==============================================================
    #             CREATION FAILURE TEST CASES
    # ==============================================================
    def test_client_creation_failure_no_protocol_client(self):
        self.assertRaises(Exception, self._create_identity_client, None, 2, 2, 30)

    # ==============================================================
    #             REQUEST RESPONSE OPERATION TEST CASES
    # ==============================================================
    def test_basic_provisioning5(self):
        self._do_identity_operation_test5(lambda identity_client: self._do_basic_provisioning_test(identity_client))

    def test_basic_provisioning311(self):
        self._do_identity_operation_test311(lambda identity_client: self._do_basic_provisioning_test(identity_client))

    def test_csr_provisioning5(self):
        self._do_identity_operation_test5(lambda identity_client: self._do_csr_provisioning_test(identity_client))

    def test_csr_provisioning311(self):
        self._do_identity_operation_test311(lambda identity_client: self._do_csr_provisioning_test(identity_client))

if __name__ == 'main':
    unittest.main()
