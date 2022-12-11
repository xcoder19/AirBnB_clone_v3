#!/usr/bin/python3
"""places route"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def get_all_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('user_id') is None:
            abort(400, description='Missing user_id')
        elif storage.get(User, body["user_id"]) is None:
            abort(404)
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = Place(**body)
            obj.city_id = city_id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
            for k, v in req.items():
                if k not in invalid:
                    setattr(place, k, v)
            storage.save()
            return jsonify(place.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
