# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
import argparse
from aws_crt import io, mqtt
from awsiot import iotshadow
import sys
import threading

parser = argparse.ArgumentParser(description="Device Shadow sample keeps a value in sync across client and server")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"w6zbse3vjd5b4p-ats.iot.us-west-2.amazonaws.com\"")
parser.add_argument('--cert', required=True, help="File path to your client certificate, in PEM format")
parser.add_argument('--key', required=True, help="File path to your private key file, in PEM format")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store")
parser.add_argument('--thing-name', required=True, help="The name assigned to your IoT Thing")
parser.add_argument('--shadow-field', default="color", help="Name of field in shadow to keep in sync")
args = parser.parse_args()

port = 443 if io.is_alpn_available() else 8883
is_connected = False
shadow_field = args.shadow_field
SHADOW_VALUE_DEFAULT = "off"

# Acquire shadow_value_lock before touching shadow_value, which may be changed from any thread
shadow_value_lock = threading.Lock()
shadow_value = None

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
client_bootstrap = io.ClientBootstrap(event_loop_group)
mqtt_client = mqtt.Client(client_bootstrap)
mqtt_connection = mqtt.Connection(mqtt_client, 'samples_client_id')
shadow_client = iotshadow.IotShadowClient(mqtt_connection)

# Function for gracefully quitting this sample
def exit(msg):
    print("Exiting:", msg)
    if is_connected:
        print("Disconnecting...")
        mqtt_connection.disconnect()
    else:
        sys.exit()

def on_connected(return_code, session_present):
    if return_code != 0:
        exit("Connection failed with code: {}".format(return_code))

    global is_connected
    is_connected = True
    print("Finished connecting!")

def on_disconnected(return_code):
    print("Disconnected with code: {}".format(return_code))
    sys.exit()

def on_get_shadow_completed(future):
    try:
        # future.result() raises exception if the operation had failed
        shadow = future.result() # type: awsiot.GetShadowResponse

        print("Finished getting initial shadow state.")

        with shadow_value_lock:
            if shadow_value is not None:
                print("  Ignoring initial query because a delta event has already been received.")
                return

        if shadow.state:
            if shadow.state.delta:
                value = shadow.state.delta.get(shadow_field)
                if value:
                    print("  Shadow contains delta value '{}'.".format(value))
                    change_shadow_value(value)
                    return

            if shadow.state.reported:
                value = shadow.state.reported.get(shadow_field)
                if value:
                    print("  Shadow contains reported value '{}'.".format(value))
                    set_local_value_due_to_initial_query(shadow.state.reported[shadow_field])
                    return

        print("  Shadow document lacks '{}' field. Setting defaults...".format(shadow_field))
        change_shadow_value(SHADOW_VALUE_DEFAULT)
        return

    except iotshadow.ErrorResponse as e:
        print("  Thing has no shadow document. Creating with defaults...")
        change_shadow_value(SHADOW_VALUE_DEFAULT)

    except Exception as e:
        exit("Error getting shadow: {}".format(repr(e)))

def on_delta_subscribe_completed(future):
    try:
        future.result() # raises exception if subscribe had failed
        print("Subscribed to shadow deltas.")
    except Exception as e:
        exit("Failed to subscribe to shadow deltas: {}".format(repr(e)))

def on_delta_received(delta):
    # type: (iotshadow.ShadowDeltaEvent) -> None
    try:
        print("Received shadow delta.")
        if shadow_field in delta.state:
            value = delta.state[shadow_field]
            if value is None:
                print("  Delta reports that '{}' was deleted. Resetting defaults...".format(shadow_field))
                change_shadow_value(SHADOW_VALUE_DEFAULT)
                return
            else:
                print("  Delta reports that desired value is '{}'. Changing local value...".format(value))
                change_shadow_value(value)
        else:
            print("  Delta did not report a change in '{}'".format(shadow_field))

    except Exception as e:
        exit("Error processing shadow delta: {}".format(repr(e)))

def on_shadow_update_completed(future):
    try:
        response = future.result() # awsiot.iotshadow.UpdateShadowResponse
        print("Finished updating reported shadow value to '{}'.".format(response.state.reported[shadow_field]))
        print("Enter desired value: ") # remind user they can input new values
    except Exception as e:
        exit("Failed to subscribe to shadow deltas: {}".format(repr(e)))

def set_local_value_due_to_initial_query(reported_value):
    with shadow_value_lock:
        global shadow_value
        shadow_value = reported_value
    print("Enter desired value: ") # remind user they can input new values

def change_shadow_value(value):
    global shadow_value
    with shadow_value_lock:
        if shadow_value == value:
            print("Local value is already '{}'.".format(value))
            print("Enter desired value: ") # remind user they can input new values
            return

        print("Changed local shadow value to '{}'.".format(value))
        shadow_value = value

    print("Updating reported shadow value to '{}'...".format(value))
    try:
        request = iotshadow.UpdateShadowRequest(
            thing_name=args.thing_name,
            state=iotshadow.ShadowState(
                reported={ shadow_field: value },
                desired={ shadow_field: value },
            )
        )
        future = shadow_client.update_shadow(request)
        future.add_done_callback(on_shadow_update_completed)
    except Exception as e:
        exit("Error issuing shadow update: {}".format(repr(e)))

# Begin async connect
print("Connecting to {} on port {}...".format(args.endpoint, port))
mqtt_connection.connect(
        host_name = args.endpoint,
        port = port,
        ca_path = args.root_ca,
        key_path = args.key,
        certificate_path = args.cert,
        on_connect=on_connected,
        on_disconnect=on_disconnected,
        use_websocket=False,
        alpn=None,
        clean_session=True,
        keep_alive=6000)

# Begin async query of the shadow's current state.
get_request = iotshadow.GetShadowRequest(thing_name=args.thing_name)
print("Getting current shadow state...")
get_future = shadow_client.get_shadow(get_request)
get_future.add_done_callback(on_get_shadow_completed)

# Subscribe to be notified when "shadow delta" changes.
# A delta event is sent when the server's "desired" value differs from the "reported" value.
print("Subscribing to shadow delta events...")
delta_request = iotshadow.SubscribeToShadowDeltasRequest(args.thing_name)
delta_handler = iotshadow.ShadowDeltaEventsHandler()
delta_handler.on_delta = on_delta_received
delta_subscribed_future = shadow_client.subscribe_to_shadow_deltas(delta_request, delta_handler)
delta_subscribed_future.add_done_callback(on_delta_subscribe_completed)

# The main thread simply reads user input.
# All callbacks occur on a thread.
while True:
    try:
        new_value = raw_input() # python 2 only
    except NameError:
        new_value = input() # python 3 only

    change_shadow_value(new_value)

