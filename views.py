from flask import Blueprint
import data
from json import dumps

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return "Homepage"

@views.route('/data')
def get_data_endpoint():
    response = data.get_data()

    return response
