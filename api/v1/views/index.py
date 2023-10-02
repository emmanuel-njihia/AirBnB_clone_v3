#!/usr/bin/python3
"""script that contains the index view for the API"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def get_status():
    """define api status"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    stats = {}
    classes = {
            'users': User,
            'states': State,
            'cities': City,
            'amenities': Amenity,
            'places': Place,
            'reviews': Review
            }
    """returns the number of each objects by type"""

    for cls in classes:
        count = storage.count(cls)
        stats[cls.lower() + 's'] = count

    return jsonify(stats)
