from flask import Blueprint
routes = Blueprint('routes', __name__)

from .orders import *
from .auth import *
