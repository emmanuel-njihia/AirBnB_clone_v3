#!/usr/bin/python3
"""script that contains API"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = storage.all('State').values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    request_json = request.get_json()

    if not request_json:
        abort(400, description="Not a JSON")

    if 'name' not in request_json:
        abort(400, description="Missing name")

    new_state = State(**request_json)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    request_json = request.get_json()

    if not request_json:
        abort(400, description="Not a JSON")

    for key, value in request_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
