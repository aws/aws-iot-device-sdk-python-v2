from awscrt.auth import AwsCredentialsProvider
from awscrt.io import ClientBootstrap, DefaultHostResolver, EventLoopGroup
from awsiot import mqtt_connection_builder
import boto3
import botocore.exceptions
import os
import unittest
import shutil
import tempfile
import uuid
import warnings

TIMEOUT = 100.0
PROXY_HOST = os.environ.get('proxyhost')
PROXY_PORT = int(os.environ.get('proxyport', '0'))

CUSTOM_AUTHORIZER_ENDPOINT = os.environ.get("CUSTOM_AUTHORIZER_ENDPOINT")
CUSTOM_AUTHORIZER_NAME_SIGNED = os.environ.get("CUSTOM_AUTHORIZER_NAME_SIGNED")
CUSTOM_AUTHORIZER_NAME_UNSIGNED = os.environ.get("CUSTOM_AUTHORIZER_NAME_UNSIGNED")
CUSTOM_AUTHORIZER_PASSWORD = os.environ.get("CUSTOM_AUTHORIZER_PASSWORD")
CUSTOM_AUTHORIZER_SIGNATURE = os.environ.get("CUSTOM_AUTHORIZER_SIGNATURE")
CUSTOM_AUTHORIZER_TOKEN_KEY_NAME = os.environ.get("CUSTOM_AUTHORIZER_TOKEN_KEY_NAME")
CUSTOM_AUTHORIZER_TOKEN_VALUE = os.environ.get("CUSTOM_AUTHORIZER_TOKEN_VALUE")


def has_custom_auth_environment():
    return (CUSTOM_AUTHORIZER_ENDPOINT is not None) and (CUSTOM_AUTHORIZER_NAME_SIGNED is not None) and \
           (CUSTOM_AUTHORIZER_NAME_UNSIGNED is not None) and (CUSTOM_AUTHORIZER_PASSWORD is not None) and \
           (CUSTOM_AUTHORIZER_SIGNATURE is not None) and (CUSTOM_AUTHORIZER_TOKEN_KEY_NAME is not None) and \
           (CUSTOM_AUTHORIZER_TOKEN_VALUE is not None)

class Config:
    cache = None

    def __init__(self, endpoint, cert, key, region, cognito_creds):
        self.cert = cert
        self.key = key
        self.endpoint = endpoint
        self.region = region
        self.cognito_creds = cognito_creds

    @staticmethod
    def get():
        """Raises SkipTest if credentials aren't set up correctly"""
        if Config.cache:
            return Config.cache

        # boto3 caches the HTTPS connection for the API calls, which appears to the unit test
        # framework as a leak, so ignore it, that's not what we're testing here
        warnings.simplefilter('ignore', ResourceWarning)

        try:
            secrets = boto3.client('secretsmanager')
            response = secrets.get_secret_value(SecretId='unit-test/endpoint')
            endpoint = response['SecretString']
            response = secrets.get_secret_value(SecretId='unit-test/certificate')
            cert = response['SecretString'].encode('utf8')
            response = secrets.get_secret_value(SecretId='unit-test/privatekey')
            key = response['SecretString'].encode('utf8')
            region = secrets.meta.region_name
            response = secrets.get_secret_value(SecretId='unit-test/cognitopool')
            cognito_pool = response['SecretString']

            cognito = boto3.client('cognito-identity')
            response = cognito.get_id(IdentityPoolId=cognito_pool)
            cognito_id = response['IdentityId']
            response = cognito.get_credentials_for_identity(IdentityId=cognito_id)
            cognito_creds = response['Credentials']

            Config.cache = Config(endpoint, cert, key, region, cognito_creds)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as ex:
            raise unittest.SkipTest("No credentials")

        return Config.cache


def create_client_id():
    return 'aws-iot-device-sdk-python-v2-unit-test-{0}'.format(uuid.uuid4())


class MqttBuilderTest(unittest.TestCase):
    def _test_connection(self, connection):
        connection.connect().result(TIMEOUT)
        connection.disconnect().result(TIMEOUT)

    def test_mtls_from_bytes(self):
        config = Config.get()
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        connection = mqtt_connection_builder.mtls_from_bytes(
            cert_bytes=config.cert,
            pri_key_bytes=config.key,
            endpoint=config.endpoint,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)
        self._test_connection(connection)

    def test_mtls_from_path(self):
        config = Config.get()
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)

        # test "from path" builder by writing secrets to tempfiles
        tmp_dirpath = tempfile.mkdtemp()
        try:
            cert_filepath = os.path.join(tmp_dirpath, 'cert')
            with open(cert_filepath, 'wb') as cert_file:
                cert_file.write(config.cert)

            key_filepath = os.path.join(tmp_dirpath, 'key')
            with open(key_filepath, 'wb') as key_file:
                key_file.write(config.key)

            connection = mqtt_connection_builder.mtls_from_path(
                cert_filepath=cert_filepath,
                pri_key_filepath=key_filepath,
                endpoint=config.endpoint,
                client_id=create_client_id(),
                client_bootstrap=bootstrap)

        finally:
            shutil.rmtree(tmp_dirpath)

        self._test_connection(connection)

    def test_websockets_default(self):
        """Websocket connection with default credentials provider"""
        config = Config.get()
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        cred_provider = AwsCredentialsProvider.new_default_chain(bootstrap)
        connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            region=config.region,
            credentials_provider=cred_provider,
            endpoint=config.endpoint,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)
        self._test_connection(connection)

    def test_websockets_sts(self):
        """Websocket connection with X-Amz-Security-Token query param"""
        config = Config.get()
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        cred_provider = AwsCredentialsProvider.new_static(
            access_key_id=config.cognito_creds['AccessKeyId'],
            secret_access_key=config.cognito_creds['SecretKey'],
            session_token=config.cognito_creds['SessionToken'])
        connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            region=config.region,
            credentials_provider=cred_provider,
            endpoint=config.endpoint,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)
        self._test_connection(connection)

    @unittest.skipIf(PROXY_HOST is None, 'requires "proxyhost" and "proxyport" env vars')
    def test_websockets_proxy(self):
        config = Config.get()
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)
        cred_provider = AwsCredentialsProvider.new_default_chain(bootstrap)
        connection = mqtt_connection_builder.websockets_with_default_aws_signing(
            credentials_provider=cred_provider,
            websocket_proxy_options=HttpProxyOptions(PROXY_HOST, PROXY_PORT),
            endpoint=config.endpoint,
            region=config.region,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)
        self._test_connection(connection)

    @unittest.skipIf(not has_custom_auth_environment(), 'requires custom authentication env vars')
    def test_mqtt311_builder_direct_signed_custom_authorizer(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)

        connection = mqtt_connection_builder.direct_with_custom_authorizer(
            auth_username="",
            auth_authorizer_name=CUSTOM_AUTHORIZER_NAME_SIGNED,
            auth_authorizer_signature=CUSTOM_AUTHORIZER_SIGNATURE,
            auth_password=CUSTOM_AUTHORIZER_PASSWORD,
            auth_token_key_name=CUSTOM_AUTHORIZER_TOKEN_KEY_NAME,
            auth_token_value=CUSTOM_AUTHORIZER_TOKEN_VALUE,
            endpoint=CUSTOM_AUTHORIZER_ENDPOINT,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)

        self._test_connection(connection)

    @unittest.skipIf(not has_custom_auth_environment(), 'requires custom authentication env vars')
    def test_mqtt311_builder_direct_unsigned_custom_authorizer(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)

        connection = mqtt_connection_builder.direct_with_custom_authorizer(
            auth_username="",
            auth_authorizer_name=CUSTOM_AUTHORIZER_NAME_SIGNED,
            auth_authorizer_signature=CUSTOM_AUTHORIZER_SIGNATURE,
            auth_password=CUSTOM_AUTHORIZER_PASSWORD,
            auth_token_key_name=CUSTOM_AUTHORIZER_TOKEN_KEY_NAME,
            auth_token_value=CUSTOM_AUTHORIZER_TOKEN_VALUE,
            endpoint=CUSTOM_AUTHORIZER_ENDPOINT,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)

        self._test_connection(connection)

    @unittest.skipIf(not has_custom_auth_environment(), 'requires custom authentication env vars')
    def test_mqtt311_builder_websocket_unsigned_custom_authorizer(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)

        connection = mqtt_connection_builder.websockets_with_custom_authorizer(
            auth_username="",
            auth_authorizer_name=CUSTOM_AUTHORIZER_NAME_UNSIGNED,
            auth_password=CUSTOM_AUTHORIZER_PASSWORD,
            endpoint=CUSTOM_AUTHORIZER_ENDPOINT,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)

        self._test_connection(connection)

    @unittest.skipIf(not has_custom_auth_environment(), 'requires custom authentication env vars')
    def test_mqtt311_builder_websocket_signed_custom_authorizer(self):
        elg = EventLoopGroup()
        resolver = DefaultHostResolver(elg)
        bootstrap = ClientBootstrap(elg, resolver)

        connection = mqtt_connection_builder.websockets_with_custom_authorizer(
            auth_username="",
            auth_authorizer_name=CUSTOM_AUTHORIZER_NAME_SIGNED,
            auth_authorizer_signature=CUSTOM_AUTHORIZER_SIGNATURE,
            auth_password=CUSTOM_AUTHORIZER_PASSWORD,
            auth_token_key_name=CUSTOM_AUTHORIZER_TOKEN_KEY_NAME,
            auth_token_value=CUSTOM_AUTHORIZER_TOKEN_VALUE,
            endpoint=CUSTOM_AUTHORIZER_ENDPOINT,
            client_id=create_client_id(),
            client_bootstrap=bootstrap)

        self._test_connection(connection)

