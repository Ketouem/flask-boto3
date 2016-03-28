from unittest import TestCase
from unittest.mock import patch
from nose.tools import assert_is_instance, assert_list_equal, eq_

from flask import Flask
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask.ext.boto3 import Boto3


@patch('boto3.client')
class TestFlaskBoto3(TestCase):

    def setUp(self):
        self.app = Flask('unit_tests')

    def test_001_populate_application_context(self, mock_client):
        self.app.config['BOTO3_SERVICES'] = ['s3', 'sqs']
        b = Boto3(self.app)
        with self.app.app_context():
            assert_is_instance(b.connections, dict)
            eq_(len(b.connections), 2)
            assert_is_instance(stack.top.boto3_cns, dict)
            eq_(len(stack.top.boto3_cns), 2)

    def test_002_instantiate_good_connectors(self, mock_client):
        self.app.config['BOTO3_SERVICES'] = ['s3', 'sqs', 'dynamodb']
        b = Boto3(self.app)
        with self.app.app_context():
            b.connections
            eq_(mock_client.call_count, 3)
            assert_list_equal(
                sorted([i[0][0] for i in mock_client.call_args_list]),
                sorted(self.app.config['BOTO3_SERVICES'])
            )

    def test_003_pass_credentials_through_app_conf(self, mock_client):
        self.app.config['BOTO3_SERVICES'] = ['s3']
        self.app.config['BOTO3_ACCESS_KEY'] = 'access'
        self.app.config['BOTO3_SECRET_KEY'] = 'secret'
        b = Boto3(self.app)
        with self.app.app_context():
            b.connections
            mock_client.assert_called_once_with(
                's3',
                aws_access_key_id='access',
                aws_secret_access_key='secret'
            )
