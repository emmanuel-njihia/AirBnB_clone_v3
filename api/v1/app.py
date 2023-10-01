#!/usr/bin/python3
"""starting the api """

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""Register blueprint to Flask instance app"""

app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False

app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown(exception):
    """Method to handle teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """method to handle 404 error"""
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    """method that handles 400 error"""
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == "__main__":
    """Host and port from environment variables"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    """Run the Flask server"""
    app.run(
        host=host, port=port, threaded=True
        )
