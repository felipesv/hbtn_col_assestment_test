#!/usr/bin/python3
"""
import all the classes and create the blueprint
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.orders import *
from api.v1.views.auth import *
from api.v1.views.users import *
