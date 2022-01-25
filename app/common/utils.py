from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash

from app.common.models import User, City, init_user


def return_error(code: int, msg: str):
    """
    Create error response
    :param code: code of the error
    :param msg: message of the error
    :return: error response
    """
    return {
        'code': code,
        'message': msg
           }, code


def return_validation_error(msg):
    """
    Create validation error response
    :param msg: message for validation error
    :return: validation error response
    """
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
    """
    Retrieve an object from the database, or None if object does not exist
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :return: First found instance of table, or None if nothing was found
    """
    return table.query.filter_by(**{field: value}).one_or_none()


def db_get_all(table):
    """
    Retrieve a list of objects from the database
    :param table: table class
    :return: List of table instances that match the provided filter
    """
    return table.query.all()


def check_city(city_name):
    """
    Check if the city is in the table City
    :param city_name: name of the city to check
    :return: True or False
    """
    city = db_get_one_or_none(City, 'id', city_name)
    return city is not None


def check_user_is_admin():
    """
    Check if the user has admin rights
    :return: True or False
    """
    user_id = get_jwt_identity()
    user = db_get_one_or_none(User, 'id', user_id)
    return user.is_admin


def get_username_case_insensitive(username):
    """
    Retrieve a user with username case-insensitive, or None if object does not exist
    :param username: username to find
    :return: user or None
    """
    from sqlalchemy import func
    return User.query.filter(func.lower(User.username) == func.lower(username)).one_or_none()


def get_email_case_insensitive(email):
    """
    Retrieve a user with email case-insensitive, or None if object does not exist
    :param email: email to find
    :return: user or None
    """
    from sqlalchemy import func
    return User.query.filter(func.lower(User.email) == func.lower(email)).one_or_none()


def register_user(values, db_session, result_schema):
    """
    Register a new user
    :param values: values for new user
    :param db_session: database session
    :param result_schema: schema of what return
    :return: result_schema with new user or errors
    """
    username = values['username']
    email = values['email']
    password = values['password']
    if not password_validator(password):
        return return_error(400, "The password must contain at least 8 characters, upper and lower case letters and a number")
    password_hash = generate_password_hash(password)

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


def password_validator(password):
    """
    Check the password for password policy. It should contain at least 8 symbols, 1 lowercase letter,
    1 uppercase letter and 1 digit
    :param password: password to check
    :return: True if password is OK, False if not
    """
    if len(password) < 8:
        return False
    lower_case = 0
    upper_case = 0
    digit = 0
    for symbol in password:
        if 'a' <= symbol <= 'z':
            lower_case += 1
        elif 'A' <= symbol <= 'Z':
            upper_case += 1
        elif '0' <= symbol <= '9':
            digit += 1
    return lower_case and upper_case and digit
