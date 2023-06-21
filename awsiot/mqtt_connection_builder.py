"""
Builder functions to create a :class:`awscrt.mqtt.Connection`, configured for use with AWS IoT Core.
The following keyword arguments are common to all builder functions:

Required Keyword Arguments:

    **endpoint** (`str`): Host name of AWS IoT server.

    **client_id** (`str`): ID to place in CONNECT packet. Must be unique across all devices/clients.
            If an ID is already in use, the other client will be disconnected.

Optional Keyword Arguments (omit, or set `None` to get default value):

    **client_bootstrap** (:class:`awscrt.io.ClientBootstrap`): Client bootstrap used to establish connection.
        The ClientBootstrap will default to the static default (Io.ClientBootstrap.get_or_create_static_default)
        if the argument is omitted or set to 'None'.

    **on_connection_interrupted** (`Callable`): Callback invoked whenever the MQTT connection is lost.
        The MQTT client will automatically attempt to reconnect.
        The function should take the following arguments return nothing:

            *   `connection` (:class:`awscrt.mqtt.Connection`): This MQTT Connection.

            *   `error` (:class:`awscrt.exceptions.AwsCrtError`): Exception which caused connection loss.

            *   `**kwargs` (dict): Forward-compatibility kwargs.

    **on_connection_resumed** (`Callable`): Callback invoked whenever the MQTT connection
        is automatically resumed. Function should take the following arguments and return nothing:

            *   `connection` (:class:`awscrt.mqtt.Connection`): This MQTT Connection

            *   `return_code` (:class:`awscrt.mqtt.ConnectReturnCode`): Connect return
                code received from the server.

            *   `session_present` (bool): True if resuming existing session. False if new session.
                Note that the server has forgotten all previous subscriptions if this is False.
                Subscriptions can be re-established via resubscribe_existing_topics().

            *   `**kwargs` (dict): Forward-compatibility kwargs.

    **on_connection_success** (`Callable`): Optional callback invoked whenever the connection successfully connects.
        The function should take the following arguments and return nothing:

            *   `connection` (:class:`awscrt.mqtt.Connection`): This MQTT Connection.

            *   `callback_data` (:class:`awscrt.mqtt.OnConnectionSuccessData`): The data returned from the connection success.

    **on_connection_failure** (`Callable`): Optional callback invoked whenever the connection fails to connect.
        The function should take the following arguments and return nothing:

            *   `connection` (:class:`awscrt.mqtt.Connection`): This MQTT Connection.

            *   `callback_data` (:class:`awscrt.mqtt.OnConnectionFailureData`): The data returned from the connection failure.

    **on_connection_closed** (`Callable`): Optional callback invoked whenever the connection has been disconnected and shutdown successfully.
        The function should take the following arguments and return nothing:

            *   `connection` (:class:`awscrt.mqtt.Connection`): This MQTT Connection.

            *   `callback_data` (:class:`awscrt.mqtt.OnConnectionClosedData`): The data returned from the connection close.

    **clean_session** (`bool`): Whether or not to start a clean session with each reconnect.
        If True, the server will forget all subscriptions with each reconnect.
        Set False to request that the server resume an existing session
        or start a new session that may be resumed after a connection loss.
        The `session_present` bool in the connection callback informs
        whether an existing session was successfully resumed.
        If an existing session is resumed, the server remembers previous subscriptions
        and sends mesages (with QoS1 or higher) that were published while the client was offline.

    **reconnect_min_timeout_secs** (`int`): Minimum time to wait between reconnect attempts.
        Must be <= `reconnect_max_timeout_secs`.
        Wait starts at min and doubles with each attempt until max is reached.

    **reconnect_max_timeout_secs** (`int`): Maximum time to wait between reconnect attempts.
        Must be >= `reconnect_min_timeout_secs`.
        Wait starts at min and doubles with each attempt until max is reached.

    **keep_alive_secs** (`int`): The keep alive value, in seconds, to send in CONNECT packet.
        A PING will automatically be sent at this interval.
        The server will assume the connection is lost if no PING is received after 1.5X this value.
        Default is 1200sec (20 minutes). This duration must be longer than ping_timeout_ms.

    **ping_timeout_ms** (`int`): Milliseconds to wait for ping response before client assumes
        the connection is invalid and attempts to reconnect.
        Default is 3000ms (3 seconds). This duration must be shorter than `keep_alive_secs`.

    **protocol_operation_timeout_ms** (`int`): Milliseconds to wait for the response to the operation
        requires response by protocol. Set to zero to disable timeout. Otherwise,
        the operation will fail if no response is received within this amount of time after
        the packet is written to the socket
        It applied to PUBLISH (QoS>0) and UNSUBSCRIBE now.

    **will** (:class:`awscrt.mqtt.Will`): Will to send with CONNECT packet. The will is
        published by the server when its connection to the client is unexpectedly lost.

    **username** (`str`): Username to connect with.

    **password** (`str`): Password to connect with.

    **port** (`int`): Override default server port.
        Default port is 443 if system supports ALPN or websockets are being used.
        Otherwise, default port is 8883.

    **tcp_connect_timeout_ms** (`int`): Milliseconds to wait for TCP connect response. Default is 5000ms (5 seconds).

    **ca_filepath** (`str`): Override default trust store with CA certificates from this PEM formatted file.

    **ca_dirpath** (`str`): Override default trust store with CA certificates loaded from this directory (Unix only).

    **ca_bytes** (`bytes`): Override default trust store with CA certificates from these PEM formatted bytes.

    **enable_metrics_collection** (`bool`): Whether to send the SDK version number in the CONNECT packet.
        Default is True.

    **http_proxy_options** (:class: 'awscrt.http.HttpProxyOptions'): HTTP proxy options to use
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import awscrt.auth
import awscrt.io
import awscrt.mqtt


def _check_required_kwargs(**kwargs):
    for required in ['endpoint', 'client_id']:
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

    ca_bytes = _get(kwargs, 'ca_bytes')
    ca_filepath = _get(kwargs, 'ca_filepath')
    ca_dirpath = _get(kwargs, 'ca_dirpath')
    if ca_bytes:
        tls_ctx_options.override_default_trust_store(ca_bytes)
    elif ca_filepath or ca_dirpath:
        tls_ctx_options.override_default_trust_store_from_path(ca_dirpath, ca_filepath)

    port = _get(kwargs, 'port')
    if port is None:
        # prefer 443, even for direct MQTT connections, since it's less likely to be blocked by firewalls
        if use_websockets or awscrt.io.is_alpn_available():
            port = 443
        else:
            port = 8883

    if port == 443 and awscrt.io.is_alpn_available() and use_custom_authorizer is False:
        tls_ctx_options.alpn_list = ['http/1.1'] if use_websockets else ['x-amzn-mqtt-ca']

    socket_options = awscrt.io.SocketOptions()
    socket_options.connect_timeout_ms = _get(kwargs, 'tcp_connect_timeout_ms', 5000)
    # These have been inconsistent between keepalive/keep_alive. Resolve both for now to ease transition.
    socket_options.keep_alive = \
        _get(kwargs, 'tcp_keep_alive', _get(kwargs, 'tcp_keepalive', False))

    socket_options.keep_alive_timeout_secs = \
        _get(kwargs, 'tcp_keep_alive_timeout_secs', _get(kwargs, 'tcp_keepalive_timeout_secs', 0))

    socket_options.keep_alive_interval_secs = \
        _get(kwargs, 'tcp_keep_alive_interval_secs', _get(kwargs, 'tcp_keepalive_interval_secs', 0))

    socket_options.keep_alive_max_probes = \
        _get(kwargs, 'tcp_keep_alive_max_probes', _get(kwargs, 'tcp_keepalive_max_probes', 0))

    username = _get(kwargs, 'username', '')
    if _get(kwargs, 'enable_metrics_collection', True):
        username += _get_metrics_str(username)

    if username == "":
        username = None

    client_bootstrap = _get(kwargs, 'client_bootstrap')
    if client_bootstrap is None:
        client_bootstrap = awscrt.io.ClientBootstrap.get_or_create_static_default()

    tls_ctx = awscrt.io.ClientTlsContext(tls_ctx_options)
    mqtt_client = awscrt.mqtt.Client(client_bootstrap, tls_ctx)

    proxy_options = kwargs.get('http_proxy_options', kwargs.get('websocket_proxy_options', None))
    return awscrt.mqtt.Connection(
        client=mqtt_client,
        on_connection_interrupted=_get(kwargs, 'on_connection_interrupted'),
        on_connection_resumed=_get(kwargs, 'on_connection_resumed'),
        client_id=_get(kwargs, 'client_id'),
        host_name=_get(kwargs, 'endpoint'),
        port=port,
        clean_session=_get(kwargs, 'clean_session', False),
        reconnect_min_timeout_secs=_get(kwargs, 'reconnect_min_timeout_secs', 5),
        reconnect_max_timeout_secs=_get(kwargs, 'reconnect_max_timeout_secs', 60),
        keep_alive_secs=_get(kwargs, 'keep_alive_secs', 1200),
        ping_timeout_ms=_get(kwargs, 'ping_timeout_ms', 3000),
        protocol_operation_timeout_ms=_get(kwargs, 'protocol_operation_timeout_ms', 0),
        will=_get(kwargs, 'will'),
        username=username,
        password=_get(kwargs, 'password'),
        socket_options=socket_options,
        use_websockets=use_websockets,
        websocket_handshake_transform=websocket_handshake_transform,
        proxy_options=proxy_options,
        on_connection_success=_get(kwargs, 'on_connection_success'),
        on_connection_failure=_get(kwargs, 'on_connection_failure'),
        on_connection_closed=_get(kwargs, 'on_connection_closed'),
    )


def mtls_from_path(cert_filepath, pri_key_filepath, **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an mTLS MQTT connection to AWS IoT.
    TLS arguments are passed as filepaths.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        cert_filepath (str): Path to certificate file.

        pri_key_filepath (str): Path to private key file.
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls_from_path(cert_filepath, pri_key_filepath)
    return _builder(tls_ctx_options, **kwargs)


def mtls_from_bytes(cert_bytes, pri_key_bytes, **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an mTLS MQTT connection to AWS IoT.
    TLS arguments are passed as in-memory bytes.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
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
                     **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an mTLS MQTT connection to AWS IoT,
    using a PKCS#11 library for private key operations.

    NOTE: Unix only

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
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

def mtls_with_pkcs12(*,
                     pkcs12_filepath: str,
                     pkcs12_password: str,
                     **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an mTLS MQTT connection to AWS IoT,
    using a PKCS#12 certificate.

    NOTE: MacOS only

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Args:
        pkcs12_filepath: Path to the PKCS12 file to use

        pkcs12_password: The password for the PKCS12 file.
    """
    _check_required_kwargs(**kwargs)

    tls_ctx_options = awscrt.io.TlsContextOptions.create_client_with_mtls_pkcs12(
        pkcs12_filepath=pkcs12_filepath,
        pkcs12_password=pkcs12_password)
    return _builder(tls_ctx_options, **kwargs)


def mtls_with_windows_cert_store_path(*,
                                      cert_store_path: str,
                                      **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an mTLS MQTT connection to AWS IoT,
    using a client certificate in a Windows certificate store.

    NOTE: Windows only

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
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
        **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an MQTT connection over websockets to AWS IoT.
    The websocket handshake is signed using credentials from the credentials_provider.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        region (str): AWS region to use when signing.

        credentials_provider (awscrt.auth.AwsCredentialsProvider): Source of AWS credentials to use when signing.

        websocket_proxy_options (awscrt.http.HttpProxyOptions): Deprecated,
            for proxy settings use `http_proxy_options` (described in
            :mod:`common arguments<awsiot.mqtt_connection_builder>`)

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
        **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an MQTT connection over websockets,
    with a custom function to transform the websocket handshake request before it is sent to the server.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        websocket_handshake_transform (Callable): Function to transform websocket handshake request.
            If provided, function is called each time a websocket connection is attempted.
            The function may modify the HTTP request before it is sent to the server.
            See :class:`awscrt.mqtt.WebsocketHandshakeTransformArgs` for more info.
            Function should take the following arguments and return nothing:

                *   `transform_args` (:class:`awscrt.mqtt.WebsocketHandshakeTransformArgs`):
                    Contains HTTP request to be transformed. Function must call
                    `transform_args.done()` when complete.

                *   `**kwargs` (dict): Forward-compatibility kwargs.

        websocket_proxy_options (awscrt.http.HttpProxyOptions):  Deprecated,
            for proxy settings use `http_proxy_options` (described in
            :mod:`common arguments<awsiot.mqtt_connection_builder>`)
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
        auth_token_key_name=None,
        auth_token_value=None,
        **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an MQTT connection using a custom
    authorizer using a direct MQTT connection. This function will set the username, port, and TLS options.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        auth_username (`str`): The username to use with the custom authorizer.
            If provided, the username given will be passed when connecting to the custom authorizer.
            If not provided, it will check to see if a username has already been set (via username="example")
            and will use that instead.  Custom authentication parameters will be appended as appropriate
            to any supplied username value.

        auth_password (`str`):  The password to use with the custom authorizer.
            If not provided, then no password will be sent in the initial CONNECT packet.

        auth_authorizer_name (`str`):  Name of the custom authorizer to use.
            Required if the endpoint does not have a default custom authorizer associated with it.  It is strongly
            suggested to URL-encode this value; the SDK will not do so for you.

        auth_authorizer_signature (`str`):  The digital signature of the token value in the `auth_token_value`
            parameter. The signature must be based on the private key associated with the custom authorizer.  The
            signature must be base64 encoded.
            Required if the custom authorizer has signing enabled.  It is strongly suggested to URL-encode this value;
            the SDK will not do so for you.

        auth_token_key_name (`str`): Key used to extract the custom authorizer token from MQTT username query-string
            properties.
            Required if the custom authorizer has signing enabled.  It is strongly suggested to URL-encode
            this value; the SDK will not do so for you.

        auth_token_value (`str`): An opaque token value. This value must be signed by the private key associated with
            the custom authorizer and the result passed in via the `auth_authorizer_signature` parameter.
            Required if the custom authorizer has signing enabled.
    """

    return _with_custom_authorizer(
        auth_username=auth_username,
        auth_authorizer_name=auth_authorizer_name,
        auth_authorizer_signature=auth_authorizer_signature,
        auth_password=auth_password,
        auth_token_key_name=auth_token_key_name,
        auth_token_value=auth_token_value,
        use_websockets=False,
        **kwargs)

def websockets_with_custom_authorizer(
        region=None,
        credentials_provider=None,
        auth_username=None,
        auth_authorizer_name=None,
        auth_authorizer_signature=None,
        auth_password=None,
        auth_token_key_name=None,
        auth_token_value=None,
        **kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, configured for an MQTT connection using a custom
    authorizer using websockets. This function will set the username, port, and TLS options.

    This function takes all :mod:`common arguments<awsiot.mqtt_connection_builder>`
    described at the top of this doc, as well as...

    Keyword Args:
        region (str): AWS region to use when signing.

        credentials_provider (awscrt.auth.AwsCredentialsProvider): Source of AWS credentials to use when signing.

        auth_username (`str`): The username to use with the custom authorizer.
            If provided, the username given will be passed when connecting to the custom authorizer.
            If not provided, it will check to see if a username has already been set (via username="example")
            and will use that instead.  Custom authentication parameters will be appended as appropriate
            to any supplied username value.

        auth_password (`str`):  The password to use with the custom authorizer.
            If not provided, then no password will be sent in the initial CONNECT packet.

        auth_authorizer_name (`str`):  Name of the custom authorizer to use.
            Required if the endpoint does not have a default custom authorizer associated with it.  It is strongly
            suggested to URL-encode this value; the SDK will not do so for you.

        auth_authorizer_signature (`str`):  The digital signature of the token value in the `auth_token_value`
            parameter. The signature must be based on the private key associated with the custom authorizer.  The
            signature must be base64 encoded.
            Required if the custom authorizer has signing enabled.  It is strongly suggested to URL-encode this value;
            the SDK will not do so for you.

        auth_token_key_name (`str`): Key used to extract the custom authorizer token from MQTT username query-string
            properties.
            Required if the custom authorizer has signing enabled.  It is strongly suggested to URL-encode
            this value; the SDK will not do so for you.

        auth_token_value (`str`): An opaque token value. This value must be signed by the private key associated with
            the custom authorizer and the result passed in via the `auth_authorizer_signature` parameter.
            Required if the custom authorizer has signing enabled.
    """

    return _with_custom_authorizer(
        auth_username=auth_username,
        auth_authorizer_name=auth_authorizer_name,
        auth_authorizer_signature=auth_authorizer_signature,
        auth_password=auth_password,
        auth_token_key_name=auth_token_key_name,
        auth_token_value=auth_token_value,
        use_websockets=True,
        websockets_region=region,
        websockets_credentials_provider=credentials_provider,
        **kwargs)


def _with_custom_authorizer(auth_username=None,
        auth_authorizer_name=None,
        auth_authorizer_signature=None,
        auth_password=None,
        auth_token_key_name=None,
        auth_token_value=None,
        use_websockets=False,
        websockets_credentials_provider=None,
        websockets_region=None,
        **kwargs) -> awscrt.mqtt.Connection:
    """
    Helper function that contains the setup needed for custom authorizers
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

    if auth_token_key_name is not None and auth_token_value is not None:
        username_string = _add_to_username_parameter(username_string, auth_token_value, auth_token_key_name + "=")

    kwargs["username"] = username_string
    kwargs["password"] = auth_password

    tls_ctx_options = awscrt.io.TlsContextOptions()
    if use_websockets == False:
        kwargs["port"] = 443
        tls_ctx_options.alpn_list = ["mqtt"]

    def _sign_websocket_handshake_request(transform_args, **kwargs):
        # transform_args need to know when transform is done
        try:
            transform_args.set_done()
        except Exception as e:
            transform_args.set_done(e)

    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=use_websockets,
                    use_custom_authorizer=True,
                    websocket_handshake_transform=_sign_websocket_handshake_request if use_websockets else None,
                    **kwargs)


def new_default_builder(**kwargs) -> awscrt.mqtt.Connection:
    """
    This builder creates an :class:`awscrt.mqtt.Connection`, without any configuration besides the default TLS context options.

    This requires setting the connection details manually by passing all the necessary data
    in :mod:`common arguments<awsiot.mqtt_connection_builder>` to make a connection.
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions()

    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=False,
                    **kwargs)
