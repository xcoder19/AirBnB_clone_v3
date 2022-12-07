from api.v1.views import app_views
from flask import Flask
app = Flask(__name__)

@app.route("/status")
def status():
    return '{"status": "OK"}'

