# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import io, http, auth
from awsiot import mqtt_connection_builder, mqtt5_client_builder
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

    """
    Returns the command if it exists and has been passed to the console, otherwise it will print the help for the sample and exit the application.
    """
    def get_command_required(self, command_name, message=None):
        if hasattr(self.parsed_commands, command_name):
            return getattr(self.parsed_commands, command_name)
        else:
            self.parser.print_help()
            print("Command --" + command_name + " required.")
            if message is not None:
                print(message)
            exit()

    """
    Returns the command if it exists and has been passed to the console, otherwise it returns whatever is passed as the default.
    """
    def get_command(self, command_name, default=None):
        if hasattr(self.parsed_commands, command_name):
            return getattr(self.parsed_commands, command_name)
        return default

    def build_pkcs11_mqtt_connection(self, on_connection_interrupted, on_connection_resumed):

        pkcs11_lib_path = self.get_command_required(self.m_cmd_pkcs11_lib)
        print(f"Loading PKCS#11 library '{pkcs11_lib_path}' ...")
        pkcs11_lib = io.Pkcs11Lib(
            file=pkcs11_lib_path,
            behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
        print("Loaded!")

        pkcs11_slot_id = None
        if (self.get_command(self.m_cmd_pkcs11_slot) != None):
            pkcs11_slot_id = int(self.get_command(self.m_cmd_pkcs11_slot))

        # Create MQTT connection
        mqtt_connection = mqtt_connection_builder.mtls_with_pkcs11(
            pkcs11_lib=pkcs11_lib,
            user_pin=self.get_command_required(self.m_cmd_pkcs11_pin),
            slot_id=pkcs11_slot_id,
            token_label=self.get_command_required(self.m_cmd_pkcs11_token),
            private_key_label=self.get_command_required(self.m_cmd_pkcs11_key),
            cert_filepath=self.get_command_required(self.m_cmd_pkcs11_cert),
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            port=self.get_command("port"),
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=self.get_command_required("client_id"),
            clean_session=False,
            keep_alive_secs=30)
        return mqtt_connection

    def build_websocket_mqtt_connection(self, on_connection_interrupted, on_connection_resumed):
        proxy_options = self.get_proxy_options_for_mqtt_connection()
        credentials_provider = auth.AwsCredentialsProvider.new_default_chain()
        mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            region=self.get_command_required(self.m_cmd_signing_region),
            credentials_provider=credentials_provider,
            http_proxy_options=proxy_options,
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=self.get_command_required("client_id"),
            clean_session=False,
            keep_alive_secs=30)
        return mqtt_connection

    def build_cognito_mqtt_connection(self, on_connection_interrupted, on_connection_resumed):
        proxy_options = self.get_proxy_options_for_mqtt_connection()

        cognito_endpoint = "cognito-identity." + self.get_command_required(self.m_cmd_signing_region) + ".amazonaws.com"
        credentials_provider = auth.AwsCredentialsProvider.new_cognito(
            endpoint=cognito_endpoint,
            identity=self.get_command_required(self.m_cmd_cognito_identity),
            tls_ctx=io.ClientTlsContext(io.TlsContextOptions()))

        mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            region=self.get_command_required(self.m_cmd_signing_region),
            credentials_provider=credentials_provider,
            http_proxy_options=proxy_options,
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=self.get_command_required("client_id"),
            clean_session=False,
            keep_alive_secs=30)
        return mqtt_connection

    def build_direct_mqtt_connection(self, on_connection_interrupted, on_connection_resumed):
        proxy_options = self.get_proxy_options_for_mqtt_connection()
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            port=self.get_command_required("port"),
            cert_filepath=self.get_command_required(self.m_cmd_cert_file),
            pri_key_filepath=self.get_command_required(self.m_cmd_key_file),
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            client_id=self.get_command_required("client_id"),
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=proxy_options)
        return mqtt_connection

    def build_mqtt_connection(self, on_connection_interrupted, on_connection_resumed):
        if self.get_command(self.m_cmd_signing_region) is not None:
            return self.build_websocket_mqtt_connection(on_connection_interrupted, on_connection_resumed)
        else:
            return self.build_direct_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    def get_proxy_options_for_mqtt_connection(self):
        proxy_options = None
        if self.parsed_commands.proxy_host and self.parsed_commands.proxy_port:
            proxy_options = http.HttpProxyOptions(
                host_name=self.parsed_commands.proxy_host,
                port=self.parsed_commands.proxy_port)
        return proxy_options

    ########################################################################
    # MQTT5
    ########################################################################

    def build_pkcs11_mqtt5_client(self,
                                  on_publish_received=None,
                                  on_lifecycle_stopped=None,
                                  on_lifecycle_attempting_connect=None,
                                  on_lifecycle_connection_success=None,
                                  on_lifecycle_connection_failure=None,
                                  on_lifecycle_disconnection=None):

        pkcs11_lib_path = self.get_command_required(self.m_cmd_pkcs11_lib)
        print(f"Loading PKCS#11 library '{pkcs11_lib_path}' ...")
        pkcs11_lib = io.Pkcs11Lib(
            file=pkcs11_lib_path,
            behavior=io.Pkcs11Lib.InitializeFinalizeBehavior.STRICT)
        print("Loaded!")

        pkcs11_slot_id = None
        if (self.get_command(self.m_cmd_pkcs11_slot) is not None):
            pkcs11_slot_id = int(self.get_command(self.m_cmd_pkcs11_slot))

        # Create MQTT5 client
        mqtt5_client = mqtt5_client_builder.mtls_with_pkcs11(
            pkcs11_lib=pkcs11_lib,
            user_pin=self.get_command_required(self.m_cmd_pkcs11_pin),
            slot_id=pkcs11_slot_id,
            token_label=self.get_command_required(self.m_cmd_pkcs11_token),
            private_key_label=self.get_command_required(self.m_cmd_pkcs11_key),
            cert_filepath=self.get_command_required(self.m_cmd_pkcs11_cert),
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            port=self.get_command("port"),
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_publish_received=on_publish_received,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_connection_failure=on_lifecycle_connection_failure,
            on_lifecycle_disconnection=on_lifecycle_disconnection,
            client_id=self.get_command("client_id"))

        return mqtt5_client

    def build_websocket_mqtt5_client(self,
                                     on_publish_received=None,
                                     on_lifecycle_stopped=None,
                                     on_lifecycle_attempting_connect=None,
                                     on_lifecycle_connection_success=None,
                                     on_lifecycle_connection_failure=None,
                                     on_lifecycle_disconnection=None):
        proxy_options = self.get_proxy_options_for_mqtt_connection()
        credentials_provider = auth.AwsCredentialsProvider.new_default_chain()
        mqtt5_client = mqtt5_client_builder.websockets_with_default_aws_signing(
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            region=self.get_command_required(self.m_cmd_signing_region),
            credentials_provider=credentials_provider,
            http_proxy_options=proxy_options,
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            on_publish_received=on_publish_received,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_connection_failure=on_lifecycle_connection_failure,
            on_lifecycle_disconnection=on_lifecycle_disconnection,
            client_id=self.get_command_required("client_id"))
        return mqtt5_client

    def build_direct_mqtt5_client(self,
                                  on_publish_received=None,
                                  on_lifecycle_stopped=None,
                                  on_lifecycle_attempting_connect=None,
                                  on_lifecycle_connection_success=None,
                                  on_lifecycle_connection_failure=None,
                                  on_lifecycle_disconnection=None):
        proxy_options = self.get_proxy_options_for_mqtt_connection()
        mqtt5_client = mqtt5_client_builder.mtls_from_path(
            endpoint=self.get_command_required(self.m_cmd_endpoint),
            port=self.get_command_required("port"),
            cert_filepath=self.get_command_required(self.m_cmd_cert_file),
            pri_key_filepath=self.get_command_required(self.m_cmd_key_file),
            ca_filepath=self.get_command(self.m_cmd_ca_file),
            http_proxy_options=proxy_options,
            on_publish_received=on_publish_received,
            on_lifecycle_stopped=on_lifecycle_stopped,
            on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
            on_lifecycle_connection_success=on_lifecycle_connection_success,
            on_lifecycle_connection_failure=on_lifecycle_connection_failure,
            on_lifecycle_disconnection=on_lifecycle_disconnection,
            client_id=self.get_command_required("client_id"))
        return mqtt5_client

    def build_mqtt5_client(self,
                           on_publish_received=None,
                           on_lifecycle_stopped=None,
                           on_lifecycle_attempting_connect=None,
                           on_lifecycle_connection_success=None,
                           on_lifecycle_connection_failure=None,
                           on_lifecycle_disconnection=None):

        if self.get_command(self.m_cmd_signing_region) is not None:
            return self.build_websocket_mqtt5_client(on_publish_received=on_publish_received,
                                                     on_lifecycle_stopped=on_lifecycle_stopped,
                                                     on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
                                                     on_lifecycle_connection_success=on_lifecycle_connection_success,
                                                     on_lifecycle_connection_failure=on_lifecycle_connection_failure,
                                                     on_lifecycle_disconnection=on_lifecycle_disconnection)
        else:
            return self.build_direct_mqtt5_client(on_publish_received=on_publish_received,
                                                  on_lifecycle_stopped=on_lifecycle_stopped,
                                                  on_lifecycle_attempting_connect=on_lifecycle_attempting_connect,
                                                  on_lifecycle_connection_success=on_lifecycle_connection_success,
                                                  on_lifecycle_connection_failure=on_lifecycle_connection_failure,
                                                  on_lifecycle_disconnection=on_lifecycle_disconnection)

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
        input_isCI : bool
        # Proxy
        input_proxyHost : str
        input_proxyPort : int
        # PubSub
        input_topic : str
        input_message : str
        input_count : int
        # Websockets
        input_signingRegion : str
        # Cognito
        input_cognitoIdentity : str
        # Custom auth
        input_customAuthUsername : str
        input_customAuthorizerName : str
        input_customAuthorizerSignature : str
        input_customAuthPassword : str
        # Fleet provisioning
        input_templateName : str
        input_templateParameters : str
        input_csrPath : str
        # Services (Shadow, Jobs, Greengrass, etc)
        input_thingName : str
        input_mode : str
        # Shared Subscription
        input_groupIdentifier : str
        # PKCS#11
        input_pkcs11LibPath : str
        input_pkcs11UserPin : str
        input_pkcs11TokenLabel : str
        input_pkcs11SlotId : int
        input_pkcs11KeyLabel : str
        # X509
        input_x509Endpoint : str
        input_x509Role : str
        input_x509ThingName : str
        input_x509Cert : str
        input_x509Key : str
        input_x509Ca : str
        # PKCS12
        input_pkcs12File : str
        input_pkcs12Password : str
        # Basic discovery
        input_maxPubOps : int
        input_printDiscoveryRespOnly : bool

        def __init__(self) -> None:
            pass

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
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, "8883"))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxyHost = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxyPort = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_isCI = cmdUtils.get_command("is_ci", None) != None
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
        cmdUtils.register_command(CommandLineUtils.m_cmd_signing_region, "<str>", "The region to connect through.", required=True)
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
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_topic = cmdUtils.get_command(CommandLineUtils.m_cmd_topic, "test/topic")
        cmdData.input_message = cmdUtils.get_command(CommandLineUtils.m_cmd_message, "Hello World! ")
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_thingName = cmdUtils.get_command_required(CommandLineUtils.m_cmd_thing_name)
        cmdData.input_mode = cmdUtils.get_command(CommandLineUtils.m_cmd_mode, "both")
        cmdData.input_signingRegion = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region)
        cmdData.input_maxPubOps = int(cmdUtils.get_command(CommandLineUtils.m_cmd_max_pub_ops, 10))
        cmdData.input_printDiscoveryRespOnly = bool(cmdUtils.get_command(CommandLineUtils.m_cmd_print_discovery_resp_only, False))
        cmdData.input_proxyHost = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxyPort = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_isCI = cmdUtils.get_command("is_ci", None) != None
        return cmdData

    def parse_sample_input_cognito_connect():
        cmdUtils = CommandLineUtils("Cognito Connect - Make a Cognito MQTT connection.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_signing_region, "<str>",
                                "The signing region used for the websocket signer",
                                True, str)
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>",
                                "Client ID to use for MQTT connection (optional, default='test-*').",
                                default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_cognito_identity, "<str>",
                                "The Cognito identity ID to use to connect via Cognito",
                                True, str)
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_signingRegion = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region)
        cmdData.input_cognitoIdentity = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cognito_identity)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxyHost = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxyPort = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_isCI = cmdUtils.get_command("is_ci", None) != None
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
        cmdData.input_signingRegion = cmdUtils.get_command_required(CommandLineUtils.m_cmd_signing_region)
        cmdData.input_customAuthorizerName = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_name)
        cmdData.input_customAuthorizerSignature = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_authorizer_signature)
        cmdData.input_customAuthPassword = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_password)
        cmdData.input_customAuthUsername = cmdUtils.get_command(CommandLineUtils.m_cmd_custom_auth_username)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_isCI = cmdUtils.get_command("is_ci", None) != None
        return cmdData


    def parse_sample_input_fleet_provisioning():
        cmdUtils = CommandLineUtils("Fleet Provisioning - Provision device using either the keys or CSR.")
        cmdUtils.add_common_mqtt_commands()
        cmdUtils.add_common_proxy_commands()
        cmdUtils.add_common_logging_commands()
        cmdUtils.add_common_key_cert_commands()
        cmdUtils.register_command(CommandLineUtils.m_cmd_client_id, "<str>", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
        cmdUtils.register_command(CommandLineUtils.m_cmd_port, "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int)
        cmdUtils.register_command(CommandLineUtils.m_cmd_csr, "<path>", "Path to CSR in Pem format (optional).")
        cmdUtils.register_command(CommandLineUtils.m_cmd_template_name, "<str>", "The name of your provisioning template.")
        cmdUtils.register_command(CommandLineUtils.m_cmd_template_parameters, "<json>", "Template parameters json.")
        # Needs to be called so the command utils parse the commands
        cmdUtils.get_args()

        cmdData = CommandLineUtils.CmdData()
        cmdData.input_endpoint = cmdUtils.get_command_required(CommandLineUtils.m_cmd_endpoint)
        cmdData.input_port = int(cmdUtils.get_command(CommandLineUtils.m_cmd_port, "8883"))
        cmdData.input_cert = cmdUtils.get_command_required(CommandLineUtils.m_cmd_cert_file)
        cmdData.input_key = cmdUtils.get_command_required(CommandLineUtils.m_cmd_key_file)
        cmdData.input_ca = cmdUtils.get_command(CommandLineUtils.m_cmd_ca_file, None)
        cmdData.input_clientId = cmdUtils.get_command(CommandLineUtils.m_cmd_client_id, "test-" + str(uuid4()))
        cmdData.input_proxyHost = cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_host)
        cmdData.input_proxyPort = int(cmdUtils.get_command(CommandLineUtils.m_cmd_proxy_port))
        cmdData.input_csrPath = cmdUtils.get_command(CommandLineUtils.m_cmd_csr, None)
        cmdData.input_templateName = cmdUtils.get_command_required(CommandLineUtils.m_cmd_template_name)
        cmdData.input_templateParameters = cmdUtils.get_command_required(CommandLineUtils.m_cmd_template_parameters)
        cmdData.input_isCI = cmdUtils.get_command("is_ci", None) != None
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
