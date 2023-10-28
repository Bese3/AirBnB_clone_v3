#!/usr/bin/python3
"""Contains all REST actions for city Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.state import State
from models.city import City
from models.user import User


@app_views.route('cities/<id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(id):
    """get all places in the city"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('places/<id>', methods=['GET'],
                 strict_slashes=False)
def get_place(id):
    """get place by thier id"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(id):
    """delete a place by thier id"""
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<id>/places', methods=['POST'])
def create_place(id):
    """create a place"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data = request.get_json()
    data['city_id'] = id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update the place info"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = {k: v for k, v in request.get_json().items()
            if k not in ['id', 'user_id', 'city_id', 'created_at',
            'updated_at']}
    for k, v in data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
