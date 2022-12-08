#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

@app_views.route("/status", strict_slashes=False)
def status():
    """status """
    return jsonify(status="OK")

@app_views.route("/stats", strict_slashes=False)
def stats():
    """stats"""
    return jsonify(storage.count())
