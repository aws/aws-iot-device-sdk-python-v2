# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import io

class CommandLineUtils:
    def __init__(self, description) -> None:
        self.parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
        self.commands = {}

    def register_command(self, command_name, example_input, help_output, required=False, type=None, default=None, choices=None, action=None):
        self.commands[command_name] = {
            "name":command_name,
            "example_input":example_input,
            "help_output":help_output,
            "required": required,
            "type": type,
            "default": default,
            "choices": choices,
            "action": action
        }

    def remove_command(self, command_name):
        if command_name in self.commands.keys():
            self.commands.pop(command_name)

    def get_args(self):
        # add all the commands
        for command in self.commands.values():
            if not command["action"] is None:
                self.parser.add_argument("--" + command["name"], action=command["action"], help=command["help_output"],
                    required=command["required"], default=command["default"])
            else:
                self.parser.add_argument("--" + command["name"], metavar=command["example_input"], help=command["help_output"],
                    required=command["required"], type=command["type"], default=command["default"], choices=command["choices"])

        return self.parser.parse_args()

    def update_command(self, command_name, new_example_input=None, new_help_output=None, new_required=None, new_type=None, new_default=None, new_action=None):
        if command_name in self.commands.keys():
            if new_example_input:
                self.commands[command_name]["example_input"] = new_example_input
            if new_help_output:
                self.commands[command_name]["help_output"] = new_help_output
            if new_required:
                self.commands[command_name]["required"] = new_required
            if new_type:
                self.commands[command_name]["type"] = new_type
            if new_default:
                self.commands[command_name]["default"] = new_default
            if new_action:
                self.commands[command_name]["action"] = new_action

    def add_common_mqtt_commands(self):
        self.register_command("endpoint", "<str>", "The endpoint of the mqtt server not including a port.", True, str)
        self.register_command("key", "<path>", "Path to your key in PEM format.", False, str)
        self.register_command("cert", "<path>", "Path to your client certificate in PEM format.", False, str)
        self.register_command("ca_file", "<path>", "Path to AmazonRootCA1.pem (optional, system trust store used by default)", False, str)

    def add_common_proxy_commands(self):
        self.register_command("proxy_host", "<str>", "Host name of the proxy server to connect through (optional)", False, str)
        self.register_command("proxy_port", "<int>", "Port of the http proxy to use (optional, default='8080')", type=int, default=8080)

    def add_common_topic_message_commands(self):
        self.register_command("topic", "<str>", "Topic to publish, subscribe to (optional, default='test/topic').", default="test/topic")
        self.register_command("message", "<str>", "The message to send in the payload (optional, default='Hello World!').", default="Hello World!")

    def add_common_websocket_commands(self):
        self.register_command("use_websocket", "", "If specified, uses a websocket over https (optional).", default=False, action="store_true")
        self.register_command("signing_region", "<str>",
            "Used for websocket signer. It should only be specified if websockets are used (optional, default='us-east-1')", default="us-east-1")

    def add_common_logging_commands(self):
        self.register_command("verbosity", "<Log Level>", "Logging level.", default=io.LogLevel.NoLogs.name, choices=[x.name for x in io.LogLevel])
