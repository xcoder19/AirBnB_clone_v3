#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify(status="OK")
