#!/usr/bin/python3
"""flask app"""
from flask import Flask ,Blueprint
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    from models import storage

    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")

    if host and port:
        app.run(host=host, port=port, threaded=True)

    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)
