import boto3
from botocore.exceptions import UnknownServiceError
from flask import _app_ctx_stack as stack
from flask import current_app


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
        app.teardown_appcontext(self.teardown)

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
        region = current_app.config.get('BOTO3_REGION')
        access_key = current_app.config.get('BOTO3_ACCESS_KEY')
        secret_key = current_app.config.get('BOTO3_SECRET_KEY')
        if access_key and secret_key:
            creds['aws_access_key_id'] = access_key
            creds['aws_secret_access_key'] = secret_key

        try:
            cns = {}
            for svc in requested_services:
                # Check for optional parameters
                params = current_app.config.get(
                            'BOTO3_OPTIONAL_PARAMS', {}
                        ).get(svc, {})
                kwargs = params.get('kwargs', {})
                kwargs.update(creds)

                args = params.get('args', [region] if region else [])

                if not(isinstance(args, list) or isinstance(args, tuple)):
                    args = [args]

                if args:
                    cns.update({svc: boto3.resource(svc, *args, **kwargs)})
                else:
                    cns.update({svc: boto3.resource(svc, **kwargs)})
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
    def resources(self):
        return self.connections

    @property
    def clients(self):
        return {
            svc: self.connections[svc].meta.client for svc in self.connections
        }

    @property
    def connections(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'boto3_cns'):
                ctx.boto3_cns = self.connect()
            return ctx.boto3_cns
