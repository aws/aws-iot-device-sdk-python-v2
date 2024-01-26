# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import io
from uuid import uuid4

class CommandLineUtils:
    def __init__(self, description) -> None:
        self.parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
        self.commands = {}
        self.parsed_commands = None

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

    """
    Returns the command if it exists and has been passed to the console, otherwise it will print the help for the sample and exit the application.
    """
    def get_command_required(self, command_name, command_name_alt = None):
        if(command_name_alt != None):
            if hasattr(self.parsed_commands, command_name_alt):
                if(getattr(self.parsed_commands, command_name_alt) != None):
                    return getattr(self.parsed_commands, command_name_alt)

        if hasattr(self.parsed_commands, command_name):
            if(getattr(self.parsed_commands, command_name) != None):
                return getattr(self.parsed_commands, command_name)

        self.parser.print_help()
        print("Command --" + command_name + " required.")
        exit()

    """
    Returns the command if it exists, has been passed to the console, and is not None. Otherwise it returns whatever is passed as the default.
    """
    def get_command(self, command_name, default=None):
        if hasattr(self.parsed_commands, command_name):
            result = getattr(self.parsed_commands, command_name)
            if (result != None):
                return result
        return default

    def get_args(self):
        # if we have already parsed, then return the cached parsed commands
        if self.parsed_commands is not None:
            return self.parsed_commands

        # add all the commands
        for command in self.commands.values():
            if not command["action"] is None:
                self.parser.add_argument("--" + command["name"], action=command["action"], help=command["help_output"],
                    required=command["required"], default=command["default"])
            else:
                self.parser.add_argument("--" + command["name"], metavar=command["example_input"], help=command["help_output"],
                    required=command["required"], type=command["type"], default=command["default"], choices=command["choices"])

        self.parsed_commands = self.parser.parse_args()
        # Automatically start logging if it is set
        if self.parsed_commands.verbosity:
            io.init_logging(getattr(io.LogLevel, self.parsed_commands.verbosity), 'stderr')

        return self.parsed_commands

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
        self.register_command(
            CommandLineUtils.m_cmd_endpoint,
            "<str>",
            "The endpoint of the mqtt server not including a port.",
            True,
            str)
        self.register_command(
            CommandLineUtils.m_cmd_ca_file,
            "<path>",
            "Path to AmazonRootCA1.pem (optional, system trust store used by default)",
            False,
            str)
        self.register_command(
            CommandLineUtils.m_cmd_is_ci,
            "<str>",
            "If present the sample will run in CI mode (optional, default='None')",
            False,
            str)

    def add_common_mqtt5_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_endpoint,
            "<str>",
            "The endpoint of the mqtt server not including a port.",
            True,
            str)
        self.register_command(
            CommandLineUtils.m_cmd_ca_file,
            "<path>",
            "Path to AmazonRootCA1.pem (optional, system trust store used by default)",
            False,
            str)
        self.register_command(
            CommandLineUtils.m_cmd_is_ci,
            "<str>",
            "If present the sample will run in CI mode (optional, default='None')",
            False,
            str)

    def add_common_proxy_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_proxy_host,
            "<str>",
            "Host name of the proxy server to connect through (optional)",
            False,
            str)
        self.register_command(
            CommandLineUtils.m_cmd_proxy_port,
            "<int>",
            "Port of the http proxy to use (optional, default='8080')",
            type=int,
            default=8080)

    def add_common_topic_message_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_topic,
            "<str>",
            "Topic to publish, subscribe to (optional, default='test/topic').",
            default="test/topic")
        self.register_command(
            CommandLineUtils.m_cmd_message,
            "<str>",
            "The message to send in the payload (optional, default='Hello World!').",
            default="Hello World! ")

    def add_common_logging_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_verbosity,
            "<Log Level>",
            "Logging level.",
            default=io.LogLevel.NoLogs.name,
            choices=[
                x.name for x in io.LogLevel])

    def add_common_key_cert_commands(self):
        self.register_command(CommandLineUtils.m_cmd_key_file, "<path>", "Path to your key in PEM format.", True, str)
        self.register_command(CommandLineUtils.m_cmd_cert_file, "<path>", "Path to your client certificate in PEM format.", True, str)

    def add_common_custom_authorizer_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_username,
            "<str>",
            "The name to send when connecting through the custom authorizer (optional)")
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_authorizer_name,
            "<str>",
            "The name of the custom authorizer to connect to (optional but required for everything but custom domains)")
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_authorizer_signature,
            "<str>",
            "The signature to send when connecting through a custom authorizer (optional)")
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_password,
            "<str>",
            "The password to send when connecting through a custom authorizer (optional)")
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_token_key_name,
            "<str>",
            "Key used to extract the custom authorizer token (optional)")
        self.register_command(
            CommandLineUtils.m_cmd_custom_auth_token_value,
            "<str>",
            "The opaque token value for the custom authorizer (optional)")

    def add_common_x509_commands(self):
        self.register_command(
            CommandLineUtils.m_cmd_x509_endpoint,
            "<str>",
            "The credentials endpoint to fetch x509 credentials from",
        )
        self.register_command(
            CommandLineUtils.m_cmd_x509_thing_name,
            "<str>",
            "Thing name to fetch x509 credentials on behalf of"
        )
        self.register_command(
            CommandLineUtils.m_cmd_x509_role_alias,
            "<str>",
            "Role alias to use with the x509 credentials provider"
        )
        self.register_command(
            CommandLineUtils.m_cmd_x509_key,
            "<path>",
            "Path to the IoT thing private key used in fetching x509 credentials"
        )
        self.register_command(
            CommandLineUtils.m_cmd_x509_cert,
            "<path>",
            "Path to the IoT thing certificate used in fetching x509 credentials"
        )

        self.register_command(
            CommandLineUtils.m_cmd_x509_ca,
            "<path>",
            "Path to the root certificate used in fetching x509 credentials"
        )

    ########################################################################
    # cmdData utils/functions
    ########################################################################

    class CmdData:
        # General use
        input_endpoint : str
        input_cert : str
        input_key : str
        input_ca : str
        input_clientId : str
        input_port : int
        input_is_ci : bool
        input_use_websockets : bool
        # Proxy
        input_proxy_host : str
        input_proxy_port : int
        # PubSub
        input_topic : str
        input_message : str
        input_count : int
        # Websockets
        input_signing_region : str
        # Cognito
        input_cognito_identity : str
        # Custom auth
        input_custom_auth_username : str
        input_custom_authorizer_name : str
        input_custom_authorizer_signature : str
        input_custom_auth_password : str
        input_custom_authorizer_token_key_name : str
        input_custom_authorizer_token_value : str
        # Fleet provisioning
        input_template_name : str
        input_template_parameters : str
        input_csr_path : str
        # Services (Shadow, Jobs, Greengrass, etc)
        input_thing_name : str
        input_mode : str
        # Shared Subscription
        input_group_identifier : str
        # PKCS#11
        input_pkcs11_lib_path : str
        input_pkcs11_user_pin : str
        input_pkcs11_token_label : str
        input_pkcs11_slot_id : int
        input_pkcs11_key_label : str
        # X509
        input_x509_endpoint : str
        input_x509_role : str
        input_x509_thing_name : str
        input_x509_cert : str
        input_x509_key : str
        input_x509_ca : str
        # Basic discovery
        input_max_pub_ops : int
        input_print_discovery_resp_only : bool
        # Jobs
        input_job_time : int
        # Shadow
        input_shadow_property : str
        input_shadow_value : str
        input_shadow_name : str
        # PKCS12
        input_pkcs12_file : str
        input_pkcs12_password : str
        # Static credentials
        input_session_token : str
        input_access_key_id : str
        input_secret_access_key : str

        def __init__(self) -> None:
            pass

        def parse_input_topic(self, cmdUtils):
            self.input_topic = cmdUtils.get_command(CommandLineUtils.m_cmd_topic, "test/topic")
            if (cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci) != None):
                self.input_topic += "/" + str(uuid4())

    def parse_sample_input_basic_connect():
        # Parse arguments
        cmdUtils = CommandLineUtils("Basic Connect - Make a MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>",
                                "Connection port for direct connection. " +
                                "AWS IoT supports 443 and 8883 (optional, default=8883).",
                                False, int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        # Needs to be called so the command utils parse the commands
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_basic_discovery():
        allowed_actions = ['both', 'publish', 'subscribe']

        cmdUtils = CommandLineUtils("Basic Discovery - Greengrass discovery example.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_topic_message_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.remove_command(CommandLineUtils.m_cmd_endpoint)
        cmdUtils.register_command(CommandLineUtils.m_cmd_thing_name, "<str>", "The name assigned to your IoT Thing", required=True)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_mode, "<mode>",
            f"The operation mode (optional, default='both').\nModes:{allowed_actions}", default='both')
        cmdUtils.register_command(CommandLineUtils.m_cmd_region, "<str>", "The region to connect through.", required=True)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_max_pub_ops, "<int>",
            "The maximum number of publish operations (optional, default='10').",
            default=10, type=int)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_print_discovery_resp_only, "", "(optional, default='False').",
            default=False, type=bool, action="store_true")
        cmdUtils.add_common_proxy_commands()
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.parse_input_topic(cmdUtils)
        cmdData.input_message = cmdUtils.get_command(CommandLineUtils.m_cmd_message, "Hello World! ")
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_thing_name = cmdUtils.get_command_required(CommandLineUtils.m_cmd_thing_name)
        cmdData.input_mode = cmdUtils.get_command(CommandLineUtils.m_cmd_mode, "both")
        cmdData.input_signing_region = cmdUtils.get_command_required(CommandLineUtils.m_cmd_region, CommandLineUtils.m_cmd_signing_region)
        cmdData.input_max_pub_ops = int(cmdUtils.get_command(CommandLineUtils.m_cmd_max_pub_ops, 10))
        cmdData.input_print_discovery_resp_only = bool(cmdUtils.get_command(CommandLineUtils.m_cmd_print_discovery_resp_only, False))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_cognito_connect():
        cmdUtils = CommandLineUtils("Cognito Connect - Make a Cognito MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_signing_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_cognito_identity, "<str>",
                                "The Cognito identity ID to use to connect via Cognito",
                                True, str)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_signing_region = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region, CommandLineUtils.m_cmd_region)
        cmdData.input_cognito_identity = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cognito_identity)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_custom_authorizer_connect():
        cmdUtils = CommandLineUtils(
            "Custom Authorizer Connect - Make a MQTT connection using a custom authorizer.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_custom_authorizer_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_custom_authorizer_name = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_name)
        cmdData.input_custom_authorizer_signature = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_signature)
        cmdData.input_custom_auth_password = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_password)
        cmdData.input_custom_auth_username = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_username)
        cmdData.input_custom_authorizer_token_key_name = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_token_key_name)
        cmdData.input_custom_authorizer_token_value = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_token_value)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_static_credentials_connect():
        cmdUtils = CommandLineUtils(
            "Static Credentials Connect - Make a MQTT connection using Static Credentials.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_session_token, "<str>", "", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_access_key_id, "<int>", "", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_secret_access_key, "<str>", "")
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_session_token = cmdUtils.get_command(CommandLineUtils.m_cmd_session_token)
        cmdData.input_access_key_id  = cmdUtils.get_command(CommandLineUtils.m_cmd_access_key_id)
        cmdData.input_secret_access_key = cmdUtils.get_command(CommandLineUtils.m_secret_access_key)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_fleet_provisioning():
        cmdUtils = CommandLineUtils("Fleet Provisioning - Provision device using either the keys or CSR.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=8883).", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_csr, "<path>", "Path to CSR in Pem format (optional).")
        cmdUtils.register_command(CommandLineUtils.m_cmd_template_name, "<str>", "The name of your provisioning template.")
        cmdUtils.register_command(CommandLineUtils.m_cmd_template_parameters, "<json>", "Template parameters json.")
        cmdUtils.register_command(CommandLineUtils.m_cmd_mqtt_version, "<int>", "MQTT Version")
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_csr_path = cmdUtils.get_command(CommandLineUtils.m_cmd_csr, None)
        cmdData.input_template_name = cmdUtils.get_command_required(CommandLineUtils.m_cmd_template_name)
        cmdData.input_template_parameters = cmdUtils.get_command_required(CommandLineUtils.m_cmd_template_parameters)
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        cmdData.input_mqtt_version = int(cmdUtils.get_command(CommandLineUtils.m_cmd_mqtt_version, 5))
        return cmdData

    def parse_sample_input_jobs():
        cmdUtils = CommandLineUtils("Jobs - Receive and execute operations on the device.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=8883).", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_thing_name, "<str>", "The name assigned to your IoT Thing", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_job_time, "<int>", "Emulate working on a job by sleeping this many seconds (optional, default='5')", default=5, type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_mqtt_version, "<int>", "mqtt version (optional, default='5')", default=5, type=int)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_thing_name = cmdUtils.get_command_required(CommandLineUtils.m_cmd_thing_name)
        cmdData.input_job_time = int(cmdUtils.get_command(CommandLineUtils.m_cmd_job_time, 5))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        cmdData.input_mqtt_version = int(cmdUtils.get_command(CommandLineUtils.m_cmd_mqtt_version, 5))
        return cmdData

    def parse_sample_input_mqtt5_custom_authorizer_connect():
        cmdUtils = CommandLineUtils(
            "Custom Authorizer Connect - Make a MQTT5 Client connection using a custom authorizer.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_custom_authorizer_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_use_websockets, "<str>", "If set, websockets will be used (optional, do not set to use direct MQTT)")
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_custom_authorizer_name = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_name)
        cmdData.input_custom_authorizer_signature = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_signature)
        cmdData.input_custom_auth_password = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_password)
        cmdData.input_custom_auth_username = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_username)
        cmdData.input_custom_authorizer_token_key_name = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_token_key_name)
        cmdData.input_custom_authorizer_token_value = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_token_value)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_use_websockets = bool(cmdUtils.get_command(CommandLineUtils.m_cmd_use_websockets, False))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_mqtt5_pkcs11_connect():
        cmdUtils = CommandLineUtils("MQTT5 PKCS11 Connect - Make a MQTT5 Client connection using PKCS11.")
        cmdUtils.add_common_mqtt5_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_cert_file, "<path>", "Path to your client certificate in PEM format.", True, str)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_port,
            "<int>",
            "Connection port. AWS IoT supports 433 and 8883 (optional, default=8883).",
            type=int)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_client_id,
            "<str>",
            "Client ID to use for MQTT5 connection (optional, default=None).",
            default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_lib, "<path>", "Path to PKCS#11 Library", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_pin, "<str>", "User PIN for logging into PKCS#11 token.", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_token, "<str>", "Label of the PKCS#11 token to use (optional).")
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_slot, "<int>", "Slot ID containing the PKCS#11 token to use (optional).", False, int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_key, "<str>", "Label of private key on the PKCS#11 token (optional).")
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_pkcs11_lib_path = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_lib)
        cmdData.input_pkcs11_user_pin = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_pin)
        cmdData.input_pkcs11_token_label = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_token)
        cmdData.input_pkcs11_slot_id = cmdUtils.get_command(CommandLineUtils.m_cmd_pkcs11_slot, None)
        cmdData.input_pkcs11_key_label = cmdUtils.get_command(CommandLineUtils.m_cmd_pkcs11_key, None)
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_mqtt5_pubsub():
        cmdUtils = CommandLineUtils("PubSub - Send and receive messages through an MQTT5 connection.")
        cmdUtils.add_common_mqtt5_commands()
        cmdUtils.add_common_topic_message_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_port,
            "<int>",
            "Connection port. AWS IoT supports 433 and 8883 (optional, default=8883).",
            type=int)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_client_id,
            "<str>",
            "Client ID to use for MQTT5 connection (optional, default=None).",
            default="test-" + str(uuid4()))
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_count,
            "<int>",
            "The number of messages to send (optional, default='10').",
            default=10,
            type=int)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_message = cmdUtils.get_command(CommandLineUtils.m_cmd_message, "Hello World! ")
        cmdData.parse_input_topic(cmdUtils)
        cmdData.input_count = int(cmdUtils.get_command(CommandLineUtils.m_cmd_count, 10))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_mqtt5_shared_subscription():
        cmdUtils = CommandLineUtils("SharedSubscription - Send and receive messages through a MQTT5 shared subscription")
        cmdUtils.add_common_mqtt5_commands()
        cmdUtils.add_common_topic_message_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_port,
            "<int>",
            "Connection port. AWS IoT supports 433 and 8883 (optional, default=8883).",
            type=int)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_client_id,
            "<str>",
            "Client ID to use for MQTT5 connection (optional, default=None)."
            "Note that '1', '2', and '3' will be added for to the given clientIDs since this sample uses 3 clients.",
            default="test-" + str(uuid4()))
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_count,
            "<int>",
            "The number of messages to send (optional, default='10').",
            default=10,
            type=int)
        cmdUtils.register_command(
            CommandLineUtils.m_cmd_group_identifier,
            "<str>",
            "The group identifier to use in the shared subscription (optional, default='python-sample')",
            default="python-sample",
            type=str)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_message = cmdUtils.get_command(CommandLineUtils.m_cmd_message, "Hello World! ")
        cmdData.parse_input_topic(cmdUtils)
        cmdData.input_count = cmdUtils.get_command(CommandLineUtils.m_cmd_count, 10)
        cmdData.input_group_identifier = cmdUtils.get_command(CommandLineUtils.m_cmd_group_identifier, "python-sample")
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_pkcs11_connect():
        cmdUtils = CommandLineUtils("PKCS11 Connect - Make a MQTT connection using PKCS11.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_cert_file, "<path>", "Path to your client certificate in PEM format.", True, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<port>",
                                "Connection port. AWS IoT supports 443 and 8883 (optional, default=8883).",
                                type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_lib, "<path>", "Path to PKCS#11 Library", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_pin, "<str>", "User PIN for logging into PKCS#11 token.", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_token, "<str>", "Label of the PKCS#11 token to use (optional).")
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_slot, "<int>", "Slot ID containing the PKCS#11 token to use (optional).", False, int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs11_key, "<str>", "Label of private key on the PKCS#11 token (optional).")
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_pkcs11_lib_path = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_lib)
        cmdData.input_pkcs11_user_pin = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_pin)
        cmdData.input_pkcs11_token_label = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs11_token)
        cmdData.input_pkcs11_slot_id = cmdUtils.get_command(CommandLineUtils.m_cmd_pkcs11_slot, None)
        cmdData.input_pkcs11_key_label = cmdUtils.get_command(CommandLineUtils.m_cmd_pkcs11_key, None)
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_pubsub():
        cmdUtils = CommandLineUtils("PubSub - Send and receive messages through an MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_topic_message_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=8883).", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_count, "<int>", "The number of messages to send (optional, default='10').", default=10, type=int)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_message = cmdUtils.get_command(CommandLineUtils.m_cmd_message, "Hello World! ")
        cmdData.parse_input_topic(cmdUtils)
        cmdData.input_count = int(cmdUtils.get_command(CommandLineUtils.m_cmd_count, 10))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_shadow():
        cmdUtils = CommandLineUtils("Shadow - Keep a property in sync between device and server.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=8883).", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_thing_name, "<str>", "The name assigned to your IoT Thing", required=True)
        cmdUtils.register_command(CommandLineUtils.m_cmd_shadow_property, "<str>", "The name of the shadow property you want to change (optional, default=''", default="")
        cmdUtils.register_command(CommandLineUtils.m_cmd_shadow_value, "<str>", "The desired value of the shadow property you want to set (optional)")
        cmdUtils.register_command(CommandLineUtils.m_cmd_shadow_name, "<str>", "Shadow name (optional, default='')", type=str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_mqtt_version, "<int>", "mqtt version (optional, default='5')", default=5, type=int)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_thing_name = cmdUtils.get_command_required(CommandLineUtils.m_cmd_thing_name)
        cmdData.input_shadow_property = cmdUtils.get_command_required(CommandLineUtils.m_cmd_shadow_property)
        cmdData.input_shadow_value = cmdUtils.get_command(CommandLineUtils.m_cmd_shadow_value, None)
        cmdData.input_shadow_name = cmdUtils.get_command(CommandLineUtils.m_cmd_shadow_name, None)
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        cmdData.input_mqtt_version = int(cmdUtils.get_command(CommandLineUtils.m_cmd_mqtt_version, 5))
        return cmdData

    def parse_sample_input_websocket_connect():
        cmdUtils = CommandLineUtils("Websocket Connect - Make a websocket MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_signing_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_signing_region = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region, CommandLineUtils.m_cmd_region)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_windows_cert_connect():
        cmdUtils = CommandLineUtils("Windows Cert Connect - Make a MQTT connection using Windows Store Certificates.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_cert_file, "<path>", "Path to certificate in Windows cert store. "
                                    "e.g. \"CurrentUser\\MY\\6ac133ac58f0a88b83e9c794eba156a98da39b4c\"", True, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_x509_connect():
        cmdUtils = CommandLineUtils("X509 Connect - Make a MQTT connection using X509.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_x509_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_signing_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_region, "<str>",
                                "The signing region used for the websocket signer",
                                False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_signing_region = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region, CommandLineUtils.m_cmd_region)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_x509_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_x509_endpoint)
        cmdData.input_x509_thing_name = cmdUtils.get_command_required(CommandLineUtils.m_cmd_x509_thing_name)
        cmdData.input_x509_role = cmdUtils.get_command_required(CommandLineUtils.m_cmd_x509_role_alias)
        cmdData.input_x509_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_x509_cert)
        cmdData.input_x509_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_x509_key)
        cmdData.input_x509_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_x509_ca, None)
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData

    def parse_sample_input_pkcs12_connect():
        # Parse arguments
        cmdUtils = CommandLineUtils("PKCS12 Connect - Make a MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs12_file, "<path>",
                                "Path to the PKCS12 file to use.", True, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_pkcs12_password, "<str>",
                                "The password for the PKCS12 file.", False, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>",
                                "Connection port for direct connection. " +
                                "AWS IoT supports 443 and 8883 (optional, default=8883).",
                                False, int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        # Needs to be called so the command utils parse the commands
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, 8883))
        cmdData.input_pkcs12_file = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs12_file)
        cmdData.input_pkcs12_password = cmdUtils.get_command_required(CommandLineUtils.m_cmd_pkcs12_password)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxy_host = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxy_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_is_ci = cmdUtils.get_command(CommandLineUtils.m_cmd_is_ci, None) != None
        return cmdData


    # Constants for commonly used/needed commands
    m_cmd_endpoint = "endpoint"
    m_cmd_ca_file = "ca_file"
    m_cmd_cert_file = "cert"
    m_cmd_key_file = "key"
    m_cmd_proxy_host = "proxy_host"
    m_cmd_proxy_port = "proxy_port"
    m_cmd_signing_region = "signing_region"
    m_cmd_pkcs11_lib = "pkcs11_lib"
    m_cmd_pkcs11_cert = "cert"
    m_cmd_pkcs11_pin = "pin"
    m_cmd_pkcs11_token = "token_label"
    m_cmd_pkcs11_slot = "slot_id"
    m_cmd_pkcs11_key = "key_label"
    m_cmd_message = "message"
    m_cmd_topic = "topic"
    m_cmd_verbosity = "verbosity"
    m_cmd_custom_auth_username = "custom_auth_username"
    m_cmd_custom_auth_authorizer_name = "custom_auth_authorizer_name"
    m_cmd_custom_auth_authorizer_signature = "custom_auth_authorizer_signature"
    m_cmd_custom_auth_password = "custom_auth_password"
    m_cmd_custom_auth_token_key_name = "custom_auth_token_key_name"
    m_cmd_custom_auth_token_value = "custom_auth_token_value"
    m_cmd_cognito_identity = "cognito_identity"
    m_cmd_x509_endpoint = "x509_endpoint"
    m_cmd_x509_thing_name = "x509_thing_name"
    m_cmd_x509_role_alias = "x509_role_alias"
    m_cmd_x509_cert = "x509_cert"
    m_cmd_x509_key = "x509_key"
    m_cmd_x509_ca = "x509_ca_file"
    m_cmd_port = "port"
    m_cmd_client_id = "client_id"
    m_cmd_is_ci = "is_ci"
    m_cmd_thing_name = "thing_name"
    m_cmd_mode = "mode"
    m_cmd_max_pub_ops = "max_pub_ops"
    m_cmd_print_discovery_resp_only = "print_discover_resp_only"
    m_cmd_csr = "csr"
    m_cmd_template_name = "template_name"
    m_cmd_template_parameters = "template_parameters"
    m_cmd_job_time = "job_time"
    m_cmd_use_websockets = "use_websockets"
    m_cmd_count = "count"
    m_cmd_group_identifier = "group_identifier"
    m_cmd_shadow_property = "shadow_property"
    m_cmd_shadow_value = "shadow_value"
    m_cmd_shadow_name = "shadow_name"
    m_cmd_pkcs12_file = "pkcs12_file"
    m_cmd_pkcs12_password = "pkcs12_password"
    m_cmd_region = "region"
    m_cmd_mqtt_version = "mqtt_version"
    m_cmd_session_token = "session_token"
    m_cmd_secret_access_key = "secret_access_key"
    m_cmd_access_key_id = "access_key_id"
