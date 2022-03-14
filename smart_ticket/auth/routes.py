from flask import Blueprint, render_template

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/')
def tryout():
    return('Hello blueprint')