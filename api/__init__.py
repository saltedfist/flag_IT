from flask import Blueprint
api = Blueprint('api', __name__)
from .admin import user