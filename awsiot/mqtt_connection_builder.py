"""
Builder functions to create a :class:`awscrt.mqtt.Connection`, configured for use with AWS IoT Core.
The following keyword arguments are common to all builder functions:

Required Keyword Arguments:

    **endpoint** (`str`): Host name of AWS IoT server.

    **client_bootstrap** (:class:`awscrt.io.ClientBootstrap`): Client bootstrap used to establish connection.

    **client_id** (`str`): ID to place in CONNECT packet. Must be unique across all devices/clients.
            If an ID is already in use, the other client will be disconnected.

Optional Keyword Arguments:

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
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import awscrt.auth
import awscrt.io
import awscrt.mqtt


def _check_required_kwargs(**kwargs):
    for required in ['client_bootstrap', 'endpoint', 'client_id']:
        if not kwargs.get(required):
            raise TypeError("Builder needs keyword-only argument '{}'".format(required))


_metrics_str = None


def _get_metrics_str():
    global _metrics_str
    if _metrics_str is None:
        try:
            import pkg_resources
            try:
                version = pkg_resources.get_distribution("awsiotsdk").version
                _metrics_str = "?SDK=PythonV2&Version={}".format(version)
            except pkg_resources.DistributionNotFound:
                _metrics_str = "?SDK=PythonV2&Version=dev"
        except BaseException:
            _metrics_str = ""

    return _metrics_str


def _builder(
        tls_ctx_options,
        use_websockets=False,
        websocket_handshake_transform=None,
        websocket_proxy_options=None,
        **kwargs):

    ca_bytes = kwargs.get('ca_bytes')
    ca_filepath = kwargs.get('ca_filepath')
    ca_dirpath = kwargs.get('ca_dirpath')
    if ca_bytes:
        tls_ctx_options.override_default_trust_store(ca_bytes)
    elif ca_filepath or ca_dirpath:
        tls_ctx_options.override_default_trust_store_from_path(ca_dirpath, ca_filepath)

    if use_websockets:
        port = 443
        if awscrt.io.is_alpn_available():
            tls_ctx_options.alpn_list = ['http/1.1']
    else:
        port = 8883
        if awscrt.io.is_alpn_available():
            port = 443
            tls_ctx_options.alpn_list = ['x-amzn-mqtt-ca']

    port = kwargs.get('port', port)

    socket_options = awscrt.io.SocketOptions()
    socket_options.connect_timeout_ms = kwargs.get('tcp_connect_timeout_ms', 5000)
    # These have been inconsistent between keepalive/keep_alive. Resolve both for now to ease transition.
    socket_options.keep_alive = kwargs.get('tcp_keep_alive', kwargs.get('tcp_keepalive', False))
    socket_options.keep_alive_timeout_secs = kwargs.get(
        'tcp_keep_alive_timeout_secs', kwargs.get(
            'tcp_keepalive_timeout_secs', 0))
    socket_options.keep_alive_interval_secs = kwargs.get(
        'tcp_keep_alive_interval_secs', kwargs.get(
            'tcp_keepalive_interval_secs', 0))
    socket_options.keep_alive_max_probes = kwargs.get(
        'tcp_keep_alive_max_probes', kwargs.get(
            'tcp_keepalive_max_probes', 0))

    username = kwargs.get('username', '')
    if kwargs.get('enable_metrics_collection', True):
        username += _get_metrics_str()

    client_bootstrap = kwargs.get('client_bootstrap')
    tls_ctx = awscrt.io.ClientTlsContext(tls_ctx_options)
    mqtt_client = awscrt.mqtt.Client(client_bootstrap, tls_ctx)

    return awscrt.mqtt.Connection(
        client=mqtt_client,
        on_connection_interrupted=kwargs.get('on_connection_interrupted'),
        on_connection_resumed=kwargs.get('on_connection_resumed'),
        client_id=kwargs.get('client_id'),
        host_name=kwargs.get('endpoint'),
        port=port,
        clean_session=kwargs.get('clean_session', False),
        reconnect_min_timeout_secs=kwargs.get('reconnect_min_timeout_secs', 5),
        reconnect_max_timeout_secs=kwargs.get('reconnect_max_timeout_secs', 60),
        keep_alive_secs=kwargs.get('keep_alive_secs', 1200),
        ping_timeout_ms=kwargs.get('ping_timeout_ms', 3000),
        protocol_operation_timeout_ms=kwargs.get('protocol_operation_timeout_ms', 0),
        will=kwargs.get('will'),
        username=username,
        password=kwargs.get('password'),
        socket_options=socket_options,
        use_websockets=use_websockets,
        websocket_handshake_transform=websocket_handshake_transform,
        websocket_proxy_options=websocket_proxy_options,
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

        websocket_proxy_options (awscrt.http.HttpProxyOptions): If specified, a proxy is used when connecting.
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

        websocket_proxy_options (awscrt.http.HttpProxyOptions): If specified, a proxy is used when connecting.
    """
    _check_required_kwargs(**kwargs)
    tls_ctx_options = awscrt.io.TlsContextOptions()
    return _builder(tls_ctx_options=tls_ctx_options,
                    use_websockets=True,
                    websocket_handshake_transform=websocket_handshake_transform,
                    websocket_proxy_options=websocket_proxy_options,
                    **kwargs)
