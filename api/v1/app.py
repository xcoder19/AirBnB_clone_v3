#!/usr/bin/python3
"""
server flask app
"""


from flask import Flask , Blueprint
from api.v1.views import app_views
from models import storage
from os import getenv




app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
   storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = getenv("HBNB_API_PORT", default='5000')

    
    app.run(host=host, port=port, threaded=True)
