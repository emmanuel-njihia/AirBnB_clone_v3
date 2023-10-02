#!/usr/bin/python3
"""script that contains the index view for the API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def get_status():
    """define api status"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    stats = {}
    classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
    """returns the number of each objects by type"""

    for cls in classes:
        count = storage.count(cls)
        stats[cls] = count

    return jsonify(stats)
