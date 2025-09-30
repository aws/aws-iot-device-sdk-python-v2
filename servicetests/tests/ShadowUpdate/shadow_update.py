# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from time import sleep
from awscrt import mqtt, mqtt5, http
from awsiot import iotshadow, mqtt_connection_builder, mqtt5_client_builder
from concurrent.futures import Future
import sys, threading, traceback
from uuid import uuid4

# - Overview -
# This sample uses the AWS IoT Device Shadow Service to keep a property in
# sync between device and server. Imagine a light whose color may be changed
# through an app, or set by a local user.
#
# - Instructions -
# Once connected, type a value in the terminal and press Enter to update
# the property's "reported" value. The sample also responds when the "desired"
# value changes on the server. To observe this, edit the Shadow document in
# the AWS Console and set a new "desired" value.
#
# - Detail -
# On startup, the sample requests the shadow document to learn the property's
# initial state. The Test subscribes to modified events from the server,
# which are sent when a property's  value  changes

# --------------------------------- ARGUMENT PARSING -----------------------------------------
import argparse, uuid

def parse_sample_input():
    parser = argparse.ArgumentParser(
        description="Shadow - Keep a property in sync between device and server.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Connection / TLS
    parser.add_argument("--endpoint", required=True, dest="input_endpoint", help="IoT endpoint hostname")
    parser.add_argument("--port", type=int, default=8883, dest="input_port", help="Port (8883 mTLS, 443 ALPN)")
    parser.add_argument("--cert", required=True, dest="input_cert",
                        help="Path to the certificate file to use during mTLS connection establishment")
    parser.add_argument("--key", required=True, dest="input_key",
                        help="Path to the private key file to use during mTLS connection establishment")
    parser.add_argument("--ca_file", dest="input_ca", help="Path to optional CA bundle (PEM)")

    # Proxy (optional)
    parser.add_argument("--proxy_host", dest="input_proxy_host", help="HTTP proxy host")
    parser.add_argument("--proxy_port", type=int, default=0, dest="input_proxy_port", help="HTTP proxy port")

    # Misc
    parser.add_argument("--client_id", dest="input_clientId",
                        default=f"test-{uuid.uuid4().hex[:8]}", help="Client ID")
    parser.add_argument("--mqtt_version", type=int, default=0, dest="input_mqtt_version", help="MQTT Version")
    parser.add_argument("--thing_name", required=True, dest="input_thing_name", help="The name assigned to your IoT Thing.")
    parser.add_argument("--shadow_property", dest="input_shadow_property", default="", 
                        help="The name of the shadow property you want to change (optional, default=''")
    parser.add_argument("--shadow_value", dest="input_shadow_value", help="The desired value of the shadow property you want to set (optional)")
    parser.add_argument("--shadow_name", dest="input_shadow_name", default="", help="Shadow name (optional, default='')")

    return parser.parse_args()

args = parse_sample_input()

# --------------------------------- ARGUMENT PARSING END -----------------------------------------

# Using globals to simplify sample code
is_sample_done = threading.Event()
mqtt_connection = None
shadow_thing_name = args.input_thing_name
shadow_property = args.input_shadow_property
mqtt_qos = None

# MQTT5 specific
mqtt5_client = None
future_connection_success = Future()
update_received = Future()


SHADOW_VALUE_DEFAULT = "off"

class LockedData:
    def __init__(self):
        self.lock = threading.Lock()
        self.shadow_value = None
        self.disconnect_called = False
        self.request_tokens = set()

locked_data = LockedData()

# Function for gracefully quitting this sample
def exit(msg_or_exception):
    if isinstance(msg_or_exception, Exception):
        print("Exiting sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    else:
        print("Exiting sample:", msg_or_exception)

    with locked_data.lock:
        if not locked_data.disconnect_called:
            locked_data.disconnect_called = True
            if args.input_mqtt_version == 5:
                print("Stop the client...")
                mqtt5_client.stop()
            else:
                print("Disconnecting...")
                future = mqtt_connection.disconnect()
                future.add_done_callback(on_disconnected)


def on_disconnected(disconnect_future):
    # type: (Future) -> None
    print("Disconnected.")

    # Signal that sample is finished
    is_sample_done.set()


def on_get_shadow_accepted(response):
    # type: (iotshadow.GetShadowResponse) -> None
    try:
        with locked_data.lock:
            # check that this is a response to a request from this session
            try:
                locked_data.request_tokens.remove(response.client_token)
            except KeyError:
                print("Ignoring get_shadow_accepted message due to unexpected token.")
                return

        if response.state:
            if response.state.delta:
                value = response.state.delta.get(shadow_property)
                if value:
                    print("  Shadow contains delta value '{}'.".format(value))
                    return

            if response.state.reported:
                value = response.state.reported.get(shadow_property)
                if value:
                    print("  Shadow contains reported value '{}'.".format(value))
                    return
        return

    except Exception as e:
        exit(e)


def on_get_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    try:
        # check that this is a response to a request from this session
        with locked_data.lock:
            try:
                locked_data.request_tokens.remove(error.client_token)
            except KeyError:
                print("Ignoring get_shadow_rejected message due to unexpected token.")
                return

        if error.code != 404:
            exit("Get request was rejected. code:{} message:'{}'".format(error.code, error.message))
    except Exception as e:
        exit(e)


def on_publish_update_shadow(future):
    # type: (Future) -> None
    try:
        future.result()
        print("Update request published.")
    except Exception as e:
        print("Failed to publish update request.")
        exit(e)


def on_update_shadow_accepted(response):
    # type: (iotshadow.UpdateShadowResponse) -> None
    try:
        # check that this is a response to a request from this session
        with locked_data.lock:
            try:
                locked_data.request_tokens.remove(response.client_token)
            except KeyError:
                print("Ignoring update_shadow_accepted message due to unexpected token.")
                return
        try:
            if response.state.reported is not None:
                if shadow_property in response.state.reported:
                    print("Finished updating reported shadow value to '{}'.".format(
                        response.state.reported[shadow_property]))  # type: ignore
                else:
                    print("Could not find shadow property with name: '{}'.".format(shadow_property))  # type: ignore
            else:
                print("Shadow states cleared.")  # when the shadow states are cleared, reported and desired are set to None
            print("1- Enter desired value: ")  # remind user they can input new values
        except BaseException:
            exit("Updated shadow is missing the target property")

    except Exception as e:
        exit(e)


def on_update_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    try:
        # check that this is a response to a request from this session
        with locked_data.lock:
            try:
                locked_data.request_tokens.remove(error.client_token)
            except KeyError:
                print("Ignoring update_shadow_rejected message due to unexpected token.")
                return

        exit("Update request was rejected. code:{} message:'{}'".format(
             error.code, error.message))

    except Exception as e:
        exit(e)


def update_event_received(response):
    print("Update Event Received\n")
    print("Current response", response.current)
    print("Previous response", response.previous)
    global update_received
    update_received.set_result(0)


# MQTT5 specific functions
# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event on Client Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Client Stopped.")
    # Signal that sample is finished
    is_sample_done.set()


def update_named_shadow():
    print("Updating named shadow")
    # named shadow here
    named_shadow = args.input_shadow_name
    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".

        print("Subscribing to Update responses...")
        update_accepted_subscribed_future, _ = shadow_client.subscribe_to_update_named_shadow_accepted(
            request=iotshadow.UpdateNamedShadowSubscriptionRequest(shadow_name=named_shadow, thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_update_shadow_accepted)

        update_rejected_subscribed_future, _ = shadow_client.subscribe_to_update_named_shadow_rejected(
            request=iotshadow.UpdateNamedShadowSubscriptionRequest(shadow_name=named_shadow, thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_update_shadow_rejected)

        # Wait for subscriptions to succeed
        update_accepted_subscribed_future.result()
        update_rejected_subscribed_future.result()

        print("Subscribing to Get responses...")
        get_accepted_subscribed_future, _ = shadow_client.subscribe_to_get_named_shadow_accepted(
            request=iotshadow.GetNamedShadowSubscriptionRequest(shadow_name=named_shadow,thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_get_shadow_accepted)

        get_rejected_subscribed_future, _ = shadow_client.subscribe_to_get_named_shadow_rejected(
            request=iotshadow.GetNamedShadowSubscriptionRequest(shadow_name=named_shadow, thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_get_shadow_rejected)

        # Wait for subscriptions to succeed
        get_accepted_subscribed_future.result()
        get_rejected_subscribed_future.result()

        # Issue request for shadow's current state.
        # The response will be received by the on_get_accepted() callback
        print("Requesting current shadow state...")

        with locked_data.lock:
            # use a unique token so we can correlate this "request" message to
            # any "response" messages received on the /accepted and /rejected topics
            token = str(uuid4())

            publish_get_future = shadow_client.publish_get_named_shadow(
                request=iotshadow.GetNamedShadowRequest(shadow_name=named_shadow, thing_name=shadow_thing_name, client_token=token),
                qos=mqtt_qos)

            locked_data.request_tokens.add(token)

        # Ensure that publish succeeds
        publish_get_future.result()

        subscribe_future, _ = shadow_client.subscribe_to_named_shadow_updated_events(
            request=iotshadow.NamedShadowUpdatedSubscriptionRequest(shadow_name=named_shadow, thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=update_event_received)
        subscribe_future.result()

        state=iotshadow.ShadowState(
            reported={shadow_property: args.input_shadow_value},
            desired={shadow_property: args.input_shadow_value},
            token=token)

        update_thing_update_future = shadow_client.publish_update_named_shadow(request = iotshadow.UpdateNamedShadowRequest
                (shadow_name = named_shadow, thing_name = shadow_thing_name, state=state), qos=mqtt_qos)

        # Wait for subscriptions to succeed
        update_thing_update_future.result()

    except Exception as e:
        exit(e)


def update_shadow():
    print("Updating classic shadow")
    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".
        print("Subscribing to Update responses...")
        update_accepted_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_accepted(
            request=iotshadow.UpdateShadowSubscriptionRequest(thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_update_shadow_accepted)

        update_rejected_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_rejected(
            request=iotshadow.UpdateShadowSubscriptionRequest(thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_update_shadow_rejected)

        # Wait for subscriptions to succeed
        update_accepted_subscribed_future.result()
        update_rejected_subscribed_future.result()

        print("Subscribing to Get responses...")
        get_accepted_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_accepted(
            request=iotshadow.GetShadowSubscriptionRequest(thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_get_shadow_accepted)

        get_rejected_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_rejected(
            request=iotshadow.GetShadowSubscriptionRequest(thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=on_get_shadow_rejected)

        # Wait for subscriptions to succeed
        get_accepted_subscribed_future.result()
        get_rejected_subscribed_future.result()

        # Issue request for shadow's current state.
        # The response will be received by the on_get_accepted() callback
        print("Requesting current shadow state...")

        with locked_data.lock:
            # use a unique token so we can correlate this "request" message to
            # any "response" messages received on the /accepted and /rejected topics
            token = str(uuid4())

            publish_get_future = shadow_client.publish_get_shadow(
                request=iotshadow.GetShadowRequest(thing_name=shadow_thing_name, client_token=token),
                qos=mqtt_qos)

            locked_data.request_tokens.add(token)

        # Ensure that publish succeeds
        publish_get_future.result()

        subscribe_future, _ = shadow_client.subscribe_to_shadow_updated_events(
            request=iotshadow.ShadowUpdatedSubscriptionRequest(thing_name=shadow_thing_name),
            qos=mqtt_qos,
            callback=update_event_received)
        subscribe_future.result()

        state=iotshadow.ShadowState(
            reported={shadow_property: args.input_shadow_value},
            desired={shadow_property: args.input_shadow_value},
            token=token)

        update_thing_update_future = shadow_client.publish_update_shadow(request = iotshadow.UpdateShadowRequest
                (thing_name = shadow_thing_name, state=state), qos=mqtt_qos)
        update_thing_update_future.result()

    except Exception as e:
        exit(e)


if __name__ == '__main__':
    # Create the proxy options if the data is present in cmdData
    proxy_options = None
    if args.input_proxy_host is not None and args.input_proxy_port != 0:
        proxy_options = http.HttpProxyOptions(
            host_name=args.input_proxy_host,
            port=args.input_proxy_port)

    if args.input_mqtt_version == 5:
        mqtt_qos = mqtt5.QoS.AT_LEAST_ONCE
        # Create a mqtt5 connection from the command line data
        mqtt5_client = mqtt5_client_builder.mtls_from_path(
            endpoint=args.input_endpoint,
            port=args.input_port,
            cert_filepath=args.input_cert,
            pri_key_filepath=args.input_key,
            ca_filepath=args.input_ca,
            client_id=args.input_clientId,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_stopped=on_lifecycle_stopped)
        print(f"Connecting to {args.input_endpoint} with client ID '{args.input_clientId}' with MQTT5...")

        mqtt5_client.start()

        shadow_client = iotshadow.IotShadowClient(mqtt5_client)
        future_connection_success.result()

        # Wait for connection to be fully established.
        # Note that it's not necessary to wait, commands issued to the
        # mqtt5_client before its fully connected will simply be queued.
        # But this sample waits here so it's obvious when a connection
        # fails or succeeds.
    elif args.input_mqtt_version == 3:
        mqtt_qos = mqtt.QoS.AT_LEAST_ONCE
        # Create a MQTT connection from the command line data
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=args.input_endpoint,
            port=args.input_port,
            cert_filepath=args.input_cert,
            pri_key_filepath=args.input_key,
            ca_filepath=args.input_ca,
            client_id=args.input_clientId,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options)

        connected_future = mqtt_connection.connect()

        shadow_client = iotshadow.IotShadowClient(mqtt_connection)

        # Wait for connection to be fully established.
        # Note that it's not necessary to wait, commands issued to the
        # mqtt_connection before its fully connected will simply be queued.
        # But this sample waits here so it's obvious when a connection
        # fails or succeeds.
        connected_future.result()
    else:
        print("Unsopported MQTT version number\n")
        sys.exit(-1)

    print("Connected!")

    if not args.input_shadow_name:
        update_shadow()
    else:
        update_named_shadow()

    print("waitin on update event\n")
    update_received.result();
    exit(0)
    # Wait for the sample to finish
    is_sample_done.wait()
