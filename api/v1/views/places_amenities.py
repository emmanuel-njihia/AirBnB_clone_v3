#!/usr/bin/python3
"""script with API for places_amenities"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, amenity_ids
from models.amenity import Amenity
from models.place import Place

"""List of allowed storage types"""
ALLOWED_STORAGE_TYPES = ['db', 'file']

"""Check storage type"""
if storage.__class__.__name__ not in ALLOWED_STORAGE_TYPES:
    raise Exception(f"Invalid storage type: {storage.__class__.__name__}")


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if storage.__class__.__name__ == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == 'file':
        amenities = [amenity.to_dict() for amenity in amenity_ids
                     if amenity in storage.all('Amenity')]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
