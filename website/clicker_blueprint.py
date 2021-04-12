import flask
from flask import request, render_template
from . import create_session
from .models.users import User
from .models.upgrades import Upgrade
from .templates import *

clicker_blueprint = flask.Blueprint('clicker_blueprint', __name__)


@clicker_blueprint.route('/start_page')
def start_page():
    return render_template('base.html')
