from flask import Flask, jsonify

from flask_boto3 import Boto3


class Config:
    DEBUG = True
    BOTO3_SERVICES = ['S3', 's3']

app = Flask(__name__)
app.config.from_object(Config)
boto_flask = Boto3(app)


@app.route("/connections")
def connections():
    return jsonify({k: str(v) for k, v in boto_flask.connections.items()})


@app.route("/clients")
def clients():
    return jsonify({k: str(v) for k, v in boto_flask.clients.items()})


@app.route("/resources")
def resources():
    return jsonify({k: str(v) for k, v in boto_flask.resources.items()})

@app.route("/buckets")
def buckets():
    return jsonify({
        "buckets": [b.name for b in boto_flask.resources['s3'].buckets.all()]
    })

if __name__ == "__main__":
    app.run()
