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

if __name__ == "__main__":
    app.run(debug=True)
