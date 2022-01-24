from flask import Blueprint, request, make_response
from app import db
from app.common.utils import return_error, db_get_one_or_none, get_username_case_insensitive, register_user, \
    return_validation_error
from app.common.models import User
from werkzeug.security import check_password_hash
from .schemas import RegistrationSchema, LoginModelSchema
from app.users.schemas import CurrentUserResponseModelSchema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, \
    create_refresh_token, set_refresh_cookies, get_jwt_identity

auth_mod = Blueprint('auth', __name__, url_prefix='')


def generate_access_token(user):
    additional_claims = {"name": user.username, "role": user.is_admin}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return access_token


def generate_refresh_token(user):
    additional_claims = {"name": user.username, "role": user.is_admin}
    refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
    return refresh_token


@auth_mod.route('/login', methods=['POST'])
def all_users():
    """
    Authenticate a user
    ---
    post:
      summary: Вход в систему
      description:
        После успешного входа в систему необходимо установить Cookies для
        пользователя
      tags:
        - auth
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
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationErrorSchema
    """
    schema = LoginModelSchema()
    try:
        values = schema.load(request.json)
    except ValidationError as ex:
        return return_validation_error(ex.messages)
    username = values['username']
    user = get_username_case_insensitive(username)

    if user is not None:
        if not check_password_hash(user.password_hash, values['password']):
            return return_error(401, 'Wrong credentials')
    else:
        return return_error(401, 'Wrong credentials')
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    result_schema = CurrentUserResponseModelSchema()
    response = make_response(result_schema.dump(user), 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@auth_mod.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    """
    Refresh cookie for current user
    ---
    post:
      summary: Обновление Cookie
      description: Пользователю обновляются Cookie
      tags:
        - auth
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=eyJ0eXAi...; Path=/; HttpOnly
          content:
            application/json:
              schema: CurrentUserResponseModelSchema
        '401':
          description: Password changed since token was issues
    """
    user_id = get_jwt_identity()
    user = db_get_one_or_none(User, 'id', user_id)
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    result_schema = CurrentUserResponseModelSchema()
    response = make_response(result_schema.dump(user), 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@auth_mod.route('/register', methods=['POST'])
def register():
    """
    Register a common user
    ---
    post:
      summary: Регистрация нового пользователя
      description: После успешной регистрации возвращаются данные пользователя
      tags:
        - auth
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
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationErrorSchema
    """
    schema = RegistrationSchema()
    try:
        values = schema.load(request.json)
    except ValidationError as ex:
        return return_error(409, ex.messages)

    return register_user(values, db.session, CurrentUserResponseModelSchema())


@auth_mod.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout current user
    ---
    post:
      summary: Выход из системы
      description: При успешном выходе необходимо удалить установленные Cookies
      tags:
        - auth
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
