#!/usr/bin/python3
"""amenity route"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.amenity import Amenity
@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET'])
def all_amenities():
    amenities = storage.all(Amenity).values()

    return jsonify([amenities.to_dict() for amenities in amenities])


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['POST'])
def post_amenity():
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = Amenity(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):

    found = storage.get(Amenity, amenity_id)
    if not found:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for k, v in req.items():
                if k not in invalid:
                    setattr(found, k, v)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
