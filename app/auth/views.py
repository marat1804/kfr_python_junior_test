from flask import Blueprint, request, make_response
from app import db
from app.common.utils import return_error, db_get_one_or_none, get_username_case_insensitive, check_city, \
    get_email_case_insensitive
from app.common.models import User, init_user, City
from werkzeug.security import generate_password_hash, check_password_hash
from .schemas import RegistrationSchema, LoginModelSchema
from app.users.schemas import CurrentUserResponseModelSchema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies

auth_mod = Blueprint('auth', __name__, url_prefix='')


def generate_access_token(user):
    additional_claims = {"name": user.username, "role": user.is_admin}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return access_token


@auth_mod.route('/login', methods=['POST'])
def all_users():
    """
    Authenticate a user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: LoginModelSchema
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
          content:
            application/json:
              schema: CurrentUserResponseModelSchema
        '400':
          description: Bad request
        '401':
          description: Wrong credentials
    """
    schema = LoginModelSchema()
    try:
        values = schema.load(request.json)
    except ValidationError as ex:
        return return_error(409, ex.messages)
    username = values['username']
    user = get_username_case_insensitive(username)

    if user is not None:
        if not check_password_hash(user.password_hash, values['password']):
            return return_error(401, 'Wrong credentials')
    else:
        return return_error(401, 'Wrong credentials')
    access_token = generate_access_token(user)
    result_schema = CurrentUserResponseModelSchema()
    response = make_response(result_schema.dump(user), 200)
    set_access_cookies(response, access_token)
    return response


@auth_mod.route('/register', methods=['POST'])
def register():
    """
    Register a common user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: RegistrationSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CurrentUserResponseModelSchema
        '400':
          description: Bad request or weak password
        '409':
          description: Username already in use
    """
    schema = RegistrationSchema()
    try:
        values = schema.load(request.json)
    except ValidationError as ex:
        return return_error(409, ex.messages)

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
            is_admin=False,
            city=values.get('city', None),
            additional_info=values.get('additional_info', None)
        )
        db.session.add(user)

    db.session.commit()
    result_schema = CurrentUserResponseModelSchema()
    return result_schema.dump(user), 200


@auth_mod.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout current user
    ---
    post:
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT
        '401':
          description: Password changed since token was issues
    """
    response = make_response({}, 200)
    unset_jwt_cookies(response)
    return response
