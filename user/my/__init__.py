from flask import Blueprint

my = Blueprint('my', __name__)

from . import alter, information, phone_identify