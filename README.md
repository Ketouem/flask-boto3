# flask-boto3

[![Circle CI](https://circleci.com/gh/Ketouem/flask-boto3.svg?style=svg)](https://circleci.com/gh/Ketouem/flask-boto3)
[![PyPI version](https://badge.fury.io/py/Flask-Boto3.svg)](https://badge.fury.io/py/Flask-Boto3)

Flask extension that ties [boto3](https://github.com/boto/boto3) connectors to the application context.
To be used with Python 3.6+.

## Install

* Via the cheeseshop
    ```bash
    $ pip install flask-boto3
    ```

* Locally with [Pipenv](https://docs.pipenv.org/)
    ```bash
    $ git clone git@github.com:Ketouem/flask-boto3.git
    $ cd flask-boto3
    flask-boto3 $ pipenv install -e .
    ```

## How-to

The main class `flask_boto3.Boto3` takes a Flask application as its contructor's parameter:

```
from flask import Flask
from flask_boto3 import Boto3
app = Flask(__name__)
app.config['BOTO3_SERVICES'] = ['s3']
boto_flask = Boto3(app)
```

Then `boto3`'s clients and resources will be available as properties within the application context:

```
>>> with app.app_context():
        print(boto_flask.clients)
        print(boto_flask.resources)
{'s3': <botocore.client.S3 object at 0x..>}
{'s3': s3.ServiceResource()}
```

## Configuration

flask-boto3 uses several keys from a Flask configuration objects to customize its behaviour:

- `BOTO3_ACCESS_KEY` & `BOTO3_SECRET_KEY` : holds the AWS credentials, if `None` the extension will rely on `boto3`'s default credentials lookup.
- `BOTO3_REGION` : holds the region that will be used for all connectors.
- `BOTO3_PROFILE` : holds the AWS profile.
- `BOTO3_SERVICES` : holds, as a list, the name of the AWS resources you want to use (e.g. `['sqs', 's3']`).
- `BOTO3_OPTIONAL_PARAMS` : useful when you need to pass additional parameters to the connectors (e.g. for testing purposes), the format is a `dict` where the top-level keys are the name of the services you're using and for each the value is a `dict` containing to keys `args` (contains the parameters as `tuple`) and `kwargs` (contains the parameters as a `dict` when they should be passed as keyword arguments).
