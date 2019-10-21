from flask import Blueprint

order = Blueprint('order', __name__)
from order import order_create, query_order, alter_order_status