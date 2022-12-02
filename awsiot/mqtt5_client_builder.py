"""
Builder functions to create a :class:`awscrt.mqtt5.Client`, configured for use with AWS IoT Core.
The following keyword arguments are common to all builder functions:

Required Keyword Arguments:

    **endpoint** (`str`): Host name of AWS IoT server.

Optional Keyword Arguments (omit, or set `None` to get default value):
    **client_options** (:class:`awscrt.mqtt5.ClientOptions`): This dataclass can be used to to apply all
            configuration options for Client creation. Any options set within will supercede defaults
            assigned by the builder. Any omitted arguments within this class will be filled by additional
            keyword arguments provided to the builder or be set to their default values.

    **connect_options** (:class:`awscrt.mqtt5.ConnectPacket`): This dataclass can be used to apply connection
            options for the client. Any options set within will supercede defaults assigned by the builder but
            will not overwrite options set by connect_options included within a client_options keyword argument.
            Any omitted arguments within this class will be assigned values of keyword arguments provided to
            the builder.

    **client_id** (`str`): ID to place in CONNECT packet. Must be unique across all devices/clients.
            If an ID is already in use, the other client will be disconnected. If one is not provided,
            AWS IoT server will assign a unique ID for use and return it in the CONNACK packet.

    **port** (`int`): Override default server port.
        Default port is 443 if system supports ALPN or websockets are being used.
        Otherwise, default port is 8883.

    **client_bootstrap** (:class:`awscrt.io.ClientBootstrap`): Client bootstrap used to establish connection.
        The ClientBootstrap will default to the static default (Io.ClientBootstrap.get_or_create_static_default)
        if the argument is omitted or set to 'None'.

    **http_proxy_options** (:class:`awscrt.http.HttpProxyOptions`): HTTP proxy options to use

    **keep_alive_interval_sec** (`int`): The maximum time interval, in seconds, that is permitted to elapse
        between the point at which the client finishes transmitting one MQTT packet and the point it starts
        sending the next.  The client will use PINGREQ packets to maintain this property. If the responding
        CONNACK contains a keep alive property value, then that is the negotiated keep alive value. Otherwise,
        the keep alive sent by the client is the negotiated value.

    **username** (`str`): Username to connect with.

    **password** (`str`): Password to connect with.

    **session_expiry_interval_sec** (`int`): A time interval, in seconds, that the client requests the server
        to persist this connection's MQTT session state for.  Has no meaning if the client has not been
        configured to rejoin sessions.  Must be non-zero in order to successfully rejoin a session. If the
        responding CONNACK contains a session expiry property value, then that is the negotiated session
        expiry value.  Otherwise, the session expiry sent by the client is the negotiated value.

    **request_response_information** (`bool`): If true, requests that the server send response information in
        the subsequent CONNACK.  This response information may be used to set up request-response implementations
        over MQTT, but doing so is outside the scope of the MQTT5 spec and client.

    **request_problem_information** (`bool`): If true, requests that the server send additional diagnostic
        information (via response string or user properties) in DISCONNECT or CONNACK packets from the server.

    **receive_maximum** (`int`): Notifies the server of the maximum number of in-flight QoS 1 and 2 messages the
        client is willing to handle.  If omitted or null, then no limit is requested.

    **maximum_packet_size** (`int`): Notifies the server of the maximum packet size the client is willing to handle.
        If omitted or null, then no limit beyond the natural limits of MQTT packet size is requested.

    **will_delay_interval_sec** (`int`): A time interval, in seconds, that the server should wait (for a session
        reconnection) before sending the will message associated with the connection's session.  If omitted or
        null, the server will send the will when the associated session is destroyed.  If the session is destroyed
        before a will delay interval has elapsed, then the will must be sent at the time of session destruction.

    **will** (:class:`awscrt.mqtt5.PublishPacket`): The definition of a message to be published when the connection's
        session is destroyed by the server or when the will delay interval has elapsed, whichever comes first.  If
        null, then nothing will be sent.

    **user_properties** (`Sequence` [:class:`awscrt.mqtt5.UserProperty`]): List of MQTT5 user properties included
        with the packet.

    **session_behavior** (:class:`awscrt.mqtt5.ClientSessionBehaviorType`): How the MQTT5 client should behave with
        respect to MQTT sessions.

    **extended_validation_and_flow_control_options** (:class:`awscrt.mqtt5.ExtendedValidationAndFlowControlOptions`):
        The additional controls for client behavior with respect to operation validation and flow control; these
        checks go beyond the base MQTT5 spec to respect limits of specific MQTT brokers. If argument is omitted or null,
        then set to AWS_IOT_CORE_DEFAULTS.

    **offline_queue_behavior** (:class:`awscrt.mqtt5.ClientOperationQueueBehaviorType`): Returns how disconnects
        affect the queued and in-progress operations tracked by the client.  Also controls how new operations are
        handled while the client is not connected.  In particular, if the client is not connected, then any operation
        that would be failed on disconnect (according to these rules) will also be rejected.

    **retry_jitter_mode** (:class:`awscrt.mqtt5.ExponentialBackoffJitterMode`): How the reconnect delay is modified
        in order to smooth out the distribution of reconnection attempt timepoints for a large set of reconnecting
        clients.

    **min_reconnect_delay_ms** (`int`): The minimum amount of time to wait to reconnect after a disconnect.
        Exponential backoff is performed with jitter after each connection failure.

    **max_reconnect_delay_ms** (`int`): The maximum amount of time to wait to reconnect after a disconnect.
    Exponential backoff is performed with jitter after each connection failure.

    **min_connected_time_to_reset_reconnect_delay_ms** (`int`): The amount of time that must elapse with an
        established connection before the reconnect delay is reset to the minimum. This helps alleviate
        bandwidth-waste in fast reconnect cycles due to permission failures on operations.

    **ping_timeout_ms** (`int`): The time interval to wait after sending a PINGREQ for a PINGRESP to arrive. If one
        does not arrive, the client will close the current connection.

    **connack_timeout_ms** (`int`): The time interval to wait after sending a CONNECT request for a CONNACK to arrive.
        If one does not arrive, the connection will be shut down.

    **ack_timeout_sec** (`int`): The time interval to wait for an ack after sending a QoS 1+ PUBLISH, SUBSCRIBE,
        or UNSUBSCRIBE before failing the operation.

    **on_publish_received** (`Callable`): Callback invoked for all publish packets received by client.
        The function should take the following arguments and return nothing:

        *   `publish_packet` (:class:`awscrt.mqtt5.PublishPacket`): Publish Packet received from the server.

    **on_lifecycle_stopped** (`Callable`): Callback invoked for Lifecycle Event Stopped.
        The function should take the following arguments and return nothing:

        *   `lifecycle_stopped_data` (:class:`awscrt.mqtt5.LifecycleStoppedData`): Currently unused dataclass.

    **on_lifecycle_attempting_connect** (`Callable`): Callback invoked for Lifecycle Event Attempting Connect.
        The function should take the following arguments and return nothing:

        *   `lifecycle_attempting_connect_data` (:class:`awscrt.mqtt5.LifecycleAttemptingConnectData`): Currently
                unused dataclass.

    **on_lifecycle_connection_success** (`Callable`): Callback invoked for Lifecycle Event Connection Success.
        The function should take the following arguments and return nothing:

        *   `lifecycle_connect_success_data` (:class:`awscrt.mqtt5.LifecycleConnectSuccessData`): Dataclass
                containing the following:

            *   `connack_packet` (:class:`awscrt.mqtt5.ConnackPacket`): Data model of an `MQTT5 CONNACK <https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901074>`_ packet.

            *   `negotiated_settings` (:class:`awscrt.mqtt5.NegotiatedSettings`): Mqtt behavior settings that have been dynamically negotiated as part of the CONNECT/CONNACK exchange.

    **on_lifecycle_connection_failure** (`Callable`): Callback invoked for Lifecycle Event Connection Failure.
        The function should take the following arguments and return nothing:

        *   `lifecycle_connection_failure_data` (:class:`awscrt.mqtt5.LifecycleConnectFailureData`): Dataclass
                containing the following:

            *   `connack_packet` (:class:`awscrt.mqtt5.ConnackPacket`): Data model of an `MQTT5 CONNACK <https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901074>`_ packet.

            *   `error_code` (`int`): Exception which caused connection failure.

    **on_lifecycle_disconnection** (`Callable`): Callback invoked for Lifecycle Event Disconnection.
        The function should take the following arguments and return nothing:

        *   `lifecycle_disconnect_data` (:class:`awscrt.mqtt5.LifecycleDisconnectData`): Dataclass
                containing the following:

            * `disconnect_packet` (:class:`awscrt.mqtt5.DisconnectPacket`): Data model of an `MQTT5 DISCONNECT <https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901205>`_ packet.

            * `error_code` (`int`): Exception which caused disconnection.

    **ca_filepath** (`str`): Override default trust store with CA certificates from this PEM formatted file.

    **ca_dirpath** (`str`): Override default trust store with CA certificates loaded from this directory (Unix only).

    **ca_bytes** (`bytes`): Override default trust store with CA certificates from these PEM formatted bytes.

    **enable_metrics_collection** (`bool`): Whether to send the SDK version number in the CONNECT packet.
        Default is True.


"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import awscrt.auth
import awscrt.io
import awscrt.mqtt5

DEFAULT_WEBSOCKET_MQTT_PORT = 443
DEFAULT_DIRECT_MQTT_PORT = 8883
DEFAULT_KEEP_ALIVE = 1200


def _check_required_kwargs(**kwargs):
    for required in ['endpoint']:
        if not kwargs.get(required):
            raise TypeError("Builder needs keyword-only argument '{}'".format(required))


def _get(kwargs, name, default=None):
    """
    Returns kwargs['name'] if it exists and is not None.
    Otherwise returns default.

    This function exists so users can pass some_arg=None to get its default
    value, instead of literally passing None.
    """
    val = kwargs.get(name)
    if val is None:
        val = default
    return val


_metrics_str = None


def _get_metrics_str(current_username=""):
    global _metrics_str

    username_has_query = False
    if current_username.find("?") != -1:
        username_has_query = True

    if _metrics_str is None:
        try:
            import pkg_resources
            try:
                version = pkg_resources.get_distribution("awsiotsdk").version
                _metrics_str = "SDK=PythonV2&Version={}".format(version)
            except pkg_resources.DistributionNotFound:
                _metrics_str = "SDK=PythonV2&Version=dev"
        except BaseException:
            _metrics_str = ""

    if not _metrics_str == "":
        if username_has_query:
            return "&" + _metrics_str
        else:
            return "?" + _metrics_str
    else:
        return ""


def _builder(
        tls_ctx_options,
        use_websockets=False,
        websocket_handshake_transform=None,
        use_custom_authorizer=False,
        **kwargs):

    username = _get(kwargs, 'username', '')
    if _get(kwargs, 'enable_metrics_collection', True):
        username += _get_metrics_str(username)

    client_options = _get(kwargs, 'client_options')
    if client_options is None:
        client_options = awscrt.mqtt5.ClientOptions(
            host_name=_get(kwargs, 'endpoint')
        )
    if client_options.connect_options is None:
        client_options.connect_options = _get(kwargs, 'connect_options', awscrt.mqtt5.ConnectPacket())

    # Client Options
    if client_options.port is None:
        client_options.port = _get(kwargs, 'port')
    if client_options.bootstrap is None:
        client_options.bootstrap = _get(kwargs, 'client_bootstrap')
    if client_options.socket_options is None:
        client_options.socket_options = _get(kwargs, 'socket_options')
    if client_options.http_proxy_options is None:
        client_options.http_proxy_options = kwargs.get(
            'http_proxy_options', kwargs.get(
                'websocket_proxy_options', None))
    if client_options.session_behavior is None:
        client_options.session_behavior = _get(kwargs, 'session_behavior')
    if client_options.extended_validation_and_flow_control_options is None:
        client_options.extended_validation_and_flow_control_options = _get(
            kwargs,
            'extended_validation_and_flow_control_options',
            default=awscrt.mqtt5.ExtendedValidationAndFlowControlOptions.AWS_IOT_CORE_DEFAULTS)
    if client_options.offline_queue_behavior is None:
        client_options.offline_queue_behavior = _get(kwargs, 'offline_queue_behavior')
    if client_options.retry_jitter_mode is None:
        client_options.retry_jitter_mode = _get(kwargs, 'retry_jitter_mode')
    if client_options.min_reconnect_delay_ms is None:
        client_options.min_reconnect_delay_ms = _get(kwargs, 'min_reconnect_delay_ms')
    if client_options.max_reconnect_delay_ms is None:
        client_options.max_reconnect_delay_ms = _get(kwargs, 'max_reconnect_delay_ms')
    if client_options.min_connected_time_to_reset_reconnect_delay_ms is None:
        client_options.min_connected_time_to_reset_reconnect_delay_ms = _get(
            kwargs, 'min_connected_time_to_reset_reconnect_delay_ms')
    if client_options.ping_timeout_ms is None:
        client_options.ping_timeout_ms = _get(kwargs, 'ping_timeout_ms')
    if client_options.connack_timeout_ms is None:
        client_options.connack_timeout_ms = _get(kwargs, 'connack_timeout_ms')
    if client_options.ack_timeout_sec is None:
        client_options.ack_timeout_sec = _get(kwargs, 'ack_timeout_sec')
    if client_options.websocket_handshake_transform is None:
        client_options.websocket_handshake_transform = websocket_handshake_transform

    # Connect Options
    if client_options.connect_options.client_id is None:
        client_options.connect_options.client_id = _get(kwargs, 'client_id')
    if client_options.connect_options.keep_alive_interval_sec is None:
        client_options.connect_options.keep_alive_interval_sec = _get(
            kwargs, 'keep_alive_interval_sec', DEFAULT_KEEP_ALIVE)
    client_options.connect_options.username = username
    if client_options.connect_options.password is None:
        client_options.connect_options.password = _get(kwargs, 'password')
    if client_options.connect_options.session_expiry_interval_sec is None:
        client_options.connect_options.session_expiry_interval_sec = _get(kwargs, 'session_expiry_interval_sec')
    if client_options.connect_options.request_response_information is None:
        client_options.connect_options.request_response_information = _get(kwargs, 'request_response_information')
    if client_options.connect_options.request_problem_information is None:
        client_options.connect_options.request_problem_information = _get(kwargs, 'request_problem_information')
    if client_options.connect_options.receive_maximum is None:
        client_options.connect_options.receive_maximum = _get(kwargs, 'receive_maximum')
    if client_options.connect_options.maximum_packet_size is None:
        client_options.connect_options.maximum_packet_size = _get(kwargs, 'maximum_packet_size')
    if client_options.connect_options.will_delay_interval_sec is None:
        client_options.connect_options.will_delay_interval_sec = _get(kwargs, 'will_delay_interval_sec')
    if client_options.connect_options.will is None:
        client_options.connect_options.will = _get(kwargs, 'will')
    if client_options.connect_options.user_properties is None:
        client_options.connect_options.user_properties = _get(kwargs, 'user_properties')

    # Callbacks
    if client_options.on_publish_callback_fn is None:
        client_options.on_publish_callback_fn = _get(kwargs, 'on_publish_received')
    if client_options.on_lifecycle_event_stopped_fn is None:
        client_options.on_lifecycle_event_stopped_fn = _get(kwargs, 'on_lifecycle_stopped')
    if client_options.on_lifecycle_event_attempting_connect_fn is None:
        client_options.on_lifecycle_event_attempting_connect_fn = _get(kwargs, 'on_lifecycle_attempting_connect')
    if client_options.on_lifecycle_event_connection_success_fn is None:
        client_options.on_lifecycle_event_connection_success_fn = _get(kwargs, 'on_lifecycle_connection_success')
    if client_options.on_lifecycle_event_connection_failure_fn is None:
        client_options.on_lifecycle_event_connection_failure_fn = _get(kwargs, 'on_lifecycle_connection_failure')
    if client_options.on_lifecycle_event_disconnection_fn is None:
        client_options.on_lifecycle_event_disconnection_fn = _get(kwargs, 'on_lifecycle_disconnection')

    ca_bytes = _get(kwargs, 'ca_bytes')
    ca_filepath = _get(kwargs, 'ca_filepath')
    ca_dirpath = _get(kwargs, 'ca_dirpath')
    if ca_bytes:
        tls_ctx_options.override_default_trust_store(ca_bytes)
    elif ca_filepath or ca_dirpath:
        tls_ctx_options.override_default_trust_store_from_path(ca_dirpath, ca_filepath)

    if client_options.port is None:
        # prefer 443, even for direct MQTT connections, since it's less likely to be blocked by firewalls
        if use_websockets or awscrt.io.is_alpn_available():
            client_options.port = DEFAULT_WEBSOCKET_MQTT_PORT
        else:
            client_options.port = DEFAULT_DIRECT_MQTT_PORT

    if client_options.port == 443 and awscrt.io.is_alpn_available() and use_custom_authorizer is False:
        tls_ctx_options.alpn_list = ['http/1.1'] if use_websockets else ['x-amzn-mqtt-ca']

    tls_ctx = awscrt.io.ClientTlsContext(tls_ctx_options)
    client_options.tls_ctx = tls_ctx
    client = awscrt.mqtt5.Client(client_options=client_options)

    return client


def mtls_from_path(cert_filepath, pri_key_filepath, **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an mTLS MQTT5 Client to AWS IoT.
    TLS arguments are passed as filepaths.

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        cert_filepath (str): Path to certificate file.

        pri_key_filepath (str): Path to private key file.
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls_from_path(cert_filepath, pri_key_filepath)
    return _builder(tls_ctx_options, **kwargs)


def mtls_from_bytes(cert_bytes, pri_key_bytes, **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an mTLS MQTT5 Client to AWS IoT.
    TLS arguments are passed as in-memory bytes.

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        cert_bytes (bytes): Certificate file bytes.

        pri_key_bytes (bytes): Private key bytes.
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls(cert_bytes, pri_key_bytes)
    return _builder(tls_ctx_options, **kwargs)


def mtls_with_pkcs11(*,
                     pkcs11_lib: awscrt.io.Pkcs11Lib,
                     user_pin: str,
                     slot_id: int = None,
                     token_label: str = None,
                     private_key_label: str = None,
                     cert_filepath: str = None,
                     cert_bytes=None,
                     **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an mTLS MQTT connection to AWS IoT,
    using a PKCS#11 library for private key operations.

    NOTE: Unix only

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Args:
        pkcs11_lib: Use this PKCS#11 library

        user_pin: User PIN, for logging into the PKCS#11 token.
            Pass `None` to log into a token with a "protected authentication path".

        slot_id: ID of slot containing PKCS#11 token.
            If not specified, the token will be chosen based on other criteria (such as token label).

        token_label: Label of the PKCS#11 token to use.
            If not specified, the token will be chosen based on other criteria (such as slot ID).

        private_key_label: Label of private key object on PKCS#11 token.
            If not specified, the key will be chosen based on other criteria
            (such as being the only available private key on the token).

        cert_filepath: Use this X.509 certificate (file on disk).
            The certificate must be PEM-formatted. The certificate may be
            specified by other means instead (ex: `cert_bytes`)

        cert_bytes (Optional[Union[str, bytes, bytearray]]):
            Use this X.509 certificate (contents in memory).
            The certificate must be PEM-formatted. The certificate may be
            specified by other means instead (ex: `cert_filepath`)
    """
    _check_required_kwargs(**kwargs)

    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls_pkcs11(
        pkcs11_lib=pkcs11_lib,
        user_pin=user_pin,
        slot_id=slot_id,
        token_label=token_label,
        private_key_label=private_key_label,
        cert_file_path=cert_filepath,
        cert_file_contents=cert_bytes)
    return _builder(tls_ctx_options, **kwargs)


def mtls_with_windows_cert_store_path(*,
                                      cert_store_path: str,
                                      **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an mTLS MQTT5 Client to AWS IoT,
    using a client certificate in a Windows certificate store.

    NOTE: Windows only

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Args:
        cert_store_path: Path to certificate in a Windows certificate store.
                The path must use backslashes and end with the certificate's thumbprint.
                Example: ``CurrentUser\\MY\\A11F8A9B5DF5B98BA3508FBCA575D09570E0D2C6``
    """
    _check_required_kwargs(**kwargs)

    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls_windows_cert_store_path(cert_store_path)
    return _builder(tls_ctx_options, **kwargs)


def websockets_with_default_aws_signing(
        region,
        credentials_provider,
        websocket_proxy_options=None,
        **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an MQTT5 Client over websockets to AWS IoT.
    The websocket handshake is signed using credentials from the credentials_provider.

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        region (str): AWS region to use when signing.

        credentials_provider (awscrt.auth.AwsCredentialsProvider): Source of AWS credentials to use when signing.

        websocket_proxy_options (awscrt.http.HttpProxyOptions): Deprecated,
            for proxy settings use `http_proxy_options` (described in
            :mod:`common arguments<awsiot.mqtt5_client_builder>`)

    """
    _check_required_kwargs(**kwargs)

    def _sign_websocket_handshake_request(transform_args, **kwargs):
        # transform_args need to know when transform is done
        try:
            signing_config = awscrt.auth.AwsSigningConfig(
                algorithm=awscrt.auth.AwsSigningAlgorithm.V4,
                signature_type=awscrt.auth.AwsSignatureType.HTTP_REQUEST_QUERY_PARAMS,
                credentials_provider=credentials_provider,
                region=region,
                service='iotdevicegateway',
                omit_session_token=True,  # IoT is weird and does not sign X-Amz-Security-Token
            )

            signing_future = awscrt.auth.aws_sign_request(transform_args.http_request, signing_config)
            signing_future.add_done_callback(lambda x: transform_args.set_done(x.exception()))
        except Exception as e:
            transform_args.set_done(e)

    return websockets_with_custom_handshake(_sign_websocket_handshake_request, websocket_proxy_options, **kwargs)


def websockets_with_custom_handshake(
        websocket_handshake_transform,
        websocket_proxy_options=None,
        **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an MQTT5 Client over websockets,
    with a custom function to transform the websocket handshake request before it is sent to the server.

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        websocket_handshake_transform (Callable): Function to transform websocket handshake request.
            If provided, function is called each time a websocket connection is attempted.
            The function may modify the HTTP request before it is sent to the server.
            See :class:`awscrt.mqtt.WebsocketHandshakeTransformArgs` for more info.
            Function should take the following arguments and return nothing:

                *   `transform_args` (:class:`awscrt.mqtt5.WebsocketHandshakeTransformArgs`):
                    Contains HTTP request to be transformed. Function must call
                    `transform_args.done()` when complete.

                *   `**kwargs` (dict): Forward-compatibility kwargs.

        websocket_proxy_options (awscrt.http.HttpProxyOptions):  Deprecated,
            for proxy settings use `http_proxy_options` (described in
            :mod:`common arguments<awsiot.mqtt5_client_builder>`)
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions()
    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=True,
                    websocket_handshake_transform=websocket_handshake_transform,
                    websocket_proxy_options=websocket_proxy_options,
                    **kwargs)


def _add_to_username_parameter(input_string, parameter_value, parameter_pretext):
    """
    Helper function to add parameters to the username in the direct_with_custom_authorizer function
    """
    return_string = input_string

    if return_string.find("?") != -1:
        return_string += "&"
    else:
        return_string += "?"

    if parameter_value.find(parameter_pretext) != -1:
        return return_string + parameter_value
    else:
        return return_string + parameter_pretext + parameter_value


def direct_with_custom_authorizer(
        auth_username=None,
        auth_authorizer_name=None,
        auth_authorizer_signature=None,
        auth_password=None,
        **kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, configured for an MQTT5 Client using a custom
    authorizer. This function will set the username, port, and TLS options.

    This function takes all :mod:`common arguments<awsiot.mqtt5_client_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        auth_username (`str`): The username to use with the custom authorizer.
            If provided, the username given will be passed when connecting to the custom authorizer.
            If not provided, it will check to see if a username has already been set (via username="example")
            and will use that instead.
            If no username has been set then no username will be sent with the MQTT connection.

        auth_authorizer_name (`str`):  The name of the custom authorizer.
            If not provided, then "x-amz-customauthorizer-name" will not be added with the MQTT connection.

        auth_authorizer_signature (`str`):  The signature of the custom authorizer.
            If not provided, then "x-amz-customauthorizer-name" will not be added with the MQTT connection.

        auth_password (`str`):  The password to use with the custom authorizer.
            If not provided, then no passord will be set.
    """

    _check_required_kwargs(**kwargs)
    username_string = ""

    if auth_username is None:
        if not _get(kwargs, "username") is None:
            username_string += _get(kwargs, "username")
    else:
        username_string += auth_username

    if auth_authorizer_name is not None:
        username_string = _add_to_username_parameter(
            username_string, auth_authorizer_name, "x-amz-customauthorizer-name=")
    if auth_authorizer_signature is not None:
        username_string = _add_to_username_parameter(
            username_string, auth_authorizer_signature, "x-amz-customauthorizer-signature=")

    kwargs["username"] = username_string
    kwargs["password"] = auth_password

    tls_ctx_options = awscrt.io.TlsContextOptions()
    tls_ctx_options.alpn_list = ["mqtt"]

    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=False,
                    use_custom_authorizer=True,
                    **kwargs)


def new_default_builder(**kwargs) -> awscrt.mqtt5.Client:
    """
    This builder creates an :class:`awscrt.mqtt5.Client`, without any configuration besides the default TLS context options.

    This requires setting the client details manually by passing all the necessary data
    in :mod:`common arguments<awsiot.mqtt5_client_builder>` to make a connection
    """
    _check_required_kwargs(kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions()
    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=False,
                    kwargs=kwargs)
