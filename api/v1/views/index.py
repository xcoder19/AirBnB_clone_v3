#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

classes = {
"amenities": "Amenity",
"cities": "City",
"places": "Place",
"reviews": "Review",
"states": "State",
"users": "User"
}
@app_views.route("/status", strict_slashes=False)
def status():
    """status """
    return jsonify(status="OK")

@app_views.route("/stats", strict_slashes=False)
def stats():
    """stats"""
    dict = {}
    for k, v in classes.items():
        dict[k] = storage.count(v)
    return jsonify(dict)
