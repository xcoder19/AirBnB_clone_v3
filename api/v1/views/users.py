#!/usr/bin/python3
"""users route"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET'])
def get_all_users():
    users = storage.all(User).values()

    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['POST'])
def post_user():
    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('email') is None:
            abort(400, description='Missing email')
        elif body.get('password') is None:
            abort(400, description='Missing password')
        else:
            obj = User(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at', 'email']
            for k, v in req.items():
                if k not in invalid:
                    setattr(user, k, v)
            storage.save()
            return jsonify(user.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
