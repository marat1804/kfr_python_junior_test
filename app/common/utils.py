from flask_jwt_extended import get_jwt_identity
from app.common.models import User, City


def return_error(code: int, msg: str):
    return {
        'code': code,
        'message': msg
           }, code


def db_get_one_or_none(table, field, value):
    return table.query.filter_by(**{field: value}).one_or_none()


def db_get_all(table):
    return table.query.all()


def check_city(city_name):
    city = db_get_one_or_none(City, 'id', city_name)
    return city is not None


def check_user_is_admin():
    user_id = get_jwt_identity()
    user = db_get_one_or_none(User, 'id', user_id)
    return user.is_admin


def get_username_case_insensitive(username):
    from sqlalchemy import func
    return User.query.filter(func.lower(User.username) == func.lower(username)).one_or_none()


def get_email_case_insensitive(email):
    from sqlalchemy import func
    return User.query.filter(func.lower(User.email) == func.lower(email)).one_or_none()
