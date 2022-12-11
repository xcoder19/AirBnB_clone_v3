#!/usr/bin/python3
"""places reviews route"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def get_all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        body = request.get_json()

        if body is None:
            abort(400, description="Not a JSON")
        elif body.get('user_id') is None:
            abort(400, description='Missing user_id')
        elif storage.get(User, body["user_id"]) is None:
            abort(404)
        elif body.get('text') is None:
            abort(400, description='Missing text')
        else:
            obj = Review(**body)
            obj.place_id = place_id
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, desciption="Not a JSON")


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
            for k, v in req.items():
                if k not in invalid:
                    setattr(review, k, v)
            storage.save()
            return jsonify(review.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
