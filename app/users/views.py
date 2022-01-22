from flask import Blueprint, request

users_mod = Blueprint('users', __name__, url_prefix='/users')


@users_mod.route('/', methods=['GET'])
def all_users():
    return {"all": "ALL"}, 200
