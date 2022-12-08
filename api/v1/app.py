#!/usr/bin/python3
"""
server flask app
"""


from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found")


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = getenv("HBNB_API_PORT", default='5000')
    app.run(host=host, port=port, threaded=True)
