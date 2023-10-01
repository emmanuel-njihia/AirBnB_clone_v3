#!/usr/bin/python3
"""starting the api """

import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

"""Register blueprint to Flask instance app"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Method to handle teardown"""
    storage.close()


if __name__ == "__main__":
    """Host and port from environment variables"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    """Run the Flask server"""
    app.run(
        host=host, port=port, threaded=True
        )
