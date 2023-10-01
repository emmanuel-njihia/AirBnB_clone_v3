#!/usr/bin/python3
"""script that contains the api blueprint"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""variable that is an instance of Blueprint"""


from api.v1.views.index import *
