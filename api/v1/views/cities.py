#!/usr/bin/python3
"""cities route """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def GET_cities():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_cities_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def POST_city():
    try:
        body = request.get_json()
        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('name') is None:
            abort(400, description='Missing name')
        else:
            obj = State(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/cities/<city_id>', methods=["PUT"])
def PUT_city(state_id):

    found = storage.get(State, state_id)
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
                    setattr(found, key, value)
            storage.save()
            return jsonify(found.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
