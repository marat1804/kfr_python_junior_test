from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash

from app.common.models import User, City, init_user


def return_error(code: int, msg: str):
    return {
        'code': code,
        'message': msg
           }, code


def return_validation_error(msg):
    json = []
    for k, v in msg.items():
        json.append({
            'loc': k,
            'msg': v[0],
            'type': v[0]
        })
    return {
               'detail': json
           }, 422


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


def register_user(values, db_session, result_schema):
    username = values['username']
    email = values['email']
    password_hash = generate_password_hash(values['password'])

    existing_user = get_username_case_insensitive(username)
    existing_email = get_email_case_insensitive(email)
    if existing_user is not None:
        return return_error(409, "Username already in use")
    elif existing_email is not None:
        return return_error(409, "Email already in use")
    else:
        city_name = values.get('city')
        if city_name is not None:
            if not check_city(city_name):
                return return_error(404, "No such city in database")
        user = init_user(
            username=username,
            password_hash=password_hash,
            first_name=values['first_name'],
            last_name=values['last_name'],
            other_name=values.get('other_name', None),
            email=values['email'],
            phone=values.get('phone', None),
            birthday=values.get('birthday', None),
            is_admin=values.get('is_admin', False),
            city=values.get('city', None),
            additional_info=values.get('additional_info', None)
        )
        db_session.add(user)

    db_session.commit()
    return result_schema.dump(user), 201
