#!/usr/bin/python3
"""script that contains the index view for the API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def get_status():
    """
    Return a JSON response with the status "OK".
    """
    data = {
        "status": "OK"
    }

    response = jsonify(data)
    response.status_code = 200

    return response


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Return JSON response with counts of different types of objects.
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    response = jsonify(data)
    response.status_code = 200

    return response
