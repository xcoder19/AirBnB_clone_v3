#!/usr/bin/python3
"""cities route """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def GET_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def GET_cities_id(city_id):
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    return jsonify([cities.to_dict() for city in cities.cities])


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = City(**body)
            obj.state_id = state.id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/cities/<city_id>', methods=["PUT"])
def put_city(city_id):
    found = storage.get(City, city_id)
    if found is None:
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
