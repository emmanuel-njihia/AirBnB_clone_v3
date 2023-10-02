#!/usr/bin/python3
"""script that contains places modules for the API"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    request_json = request.get_json()

    if not request_json:
        abort(400, description="Not a JSON")

    if 'user_id' not in request_json:
        abort(400, description="Missing user_id")

    user_id = request_json['user_id']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if 'name' not in request_json:
        abort(400, description="Missing name")

    request_json['city_id'] = city_id
    new_place = Place(**request_json)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    request_json = request.get_json()

    if not request_json:
        abort(400, description="Not a JSON")

    for key, value in request_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict()), 200
