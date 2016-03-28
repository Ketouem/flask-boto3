import boto3
from botocore.exceptions import UnknownServiceError
from flask import current_app
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class Boto3(object):
    """Stores a bunch of boto3 conectors inside Flask's application context
    for easier handling inside view functions.

    All connectors are stored inside the dict `boto3_cns` where the keys are
    the name of the services and the values their associated boto3 client.
    """

    def __init__(self, app=None):
        self.app = app
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        """Iterate through the application configuration and instantiate
        the services.
        """
        requested_services = set(
            svc.lower() for svc in current_app.config.get('BOTO3_SERVICES', [])
        )

        creds = {
            'aws_access_key_id': None,
            'aws_secret_access_key': None
        }
        access_key = current_app.config.get('BOTO3_ACCESS_KEY')
        secret_key = current_app.config.get('BOTO3_SECRET_KEY')
        if access_key and secret_key:
            creds['aws_access_key_id'] = access_key
            creds['aws_secret_access_key'] = secret_key

        try:
            cns = {
                svc: boto3.client(svc, **creds)
                for svc in requested_services
            }
        except UnknownServiceError:
            raise
        return cns

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'boto3_cns'):
            for c in ctx.boto3_cns:
                con = ctx.boto3_cns[c]
                if hasattr(con, 'close') and callable(con.close):
                    ctx.boto3_cns[c].close()

    @property
    def connections(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'boto3_cns'):
                ctx.boto3_cns = self.connect()
            return ctx.boto3_cns
