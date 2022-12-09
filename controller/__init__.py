from flask import Blueprint

routes = Blueprint('routes', __name__)

from .login_route import *
from .sign_route import *
from .select_route import *
