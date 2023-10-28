#!/usr/bin/python3
"""Contains all REST actions for city Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviwes(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    ignore_key = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_key:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
