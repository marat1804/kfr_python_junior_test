from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from app import db
from app.common.model_schemas import UserSchema, CitySchema
from app.common.utils import db_get_one_or_none, db_get_all, return_error, check_user_is_admin, \
    get_username_case_insensitive, check_city, get_email_case_insensitive
from app.common.models import User, City, init_user
from app.private.schemas import PrivateCreateUserModelSchema, PrivateDetailUserResponseModelSchema, \
    PrivateShortenInfoModelSchema
from app.users.schemas import CurrentUserResponseModelSchema, RequestUsersInQuerySchema, ShortenUserInfo, \
    PatchUserPersonalInfoSchema, UpdateUserResponseModelSchema

private_mod = Blueprint('private', __name__, url_prefix='/private')


@private_mod.route('/users', methods=['GET'])
@jwt_required()
def get_user_list():
    """
    get:
      parameters:
        - required: true
          schema:
            title: Page
            type: integer
          name: page
          in: query
        - required: true
          schema:
            title: Size
            type: integer
          name: size
          in: query
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: PrivateUsersListResponseModelSchema
        '400':
          description: Bad Request
          content:
            application/json:
              schema: ErrorResponseModelSchema
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                title: Response 401 Users Users Get
                type: string
        '422':
          description: Validation Error
          content:
            application/json:
              schema: ErrorResponseModelSchema
    """
    if not check_user_is_admin():
        return return_error(403, "User is not admin")
    try:
        request_schema = RequestUsersInQuerySchema().load(request.args)
    except ValidationError as ex:
        return return_error(409, ex.messages)
    page = request_schema.get('page', None)
    size = request_schema.get('size', None)
    users = db_get_all(User)
    users_list = users[(page - 1) * size:page * size]
    city_list = [user.city for user in users_list]
    cities = [db_get_one_or_none(City, 'id', id_) for id_ in city_list]
    response = {
        "data": PrivateShortenInfoModelSchema(many=True).dump(users_list),
        "meta": {
            "pagination": {
                "total": len(users),
                "page": page,
                "size": size
            },
            "hint": {
                "city": CitySchema(many=True).dump(cities)
            }
        }
    }
    return response, 200


@private_mod.route('/users', methods=['POST'])
@jwt_required()
def private_register_user():
    """
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: PrivateCreateUserModelSchema
      responses:
        '201':
          description: Successful Response
          content:
            application/json:
              schema: PrivateDetailUserResponseModelSchema
        '400':
          description: Bad Request
          content:
            application/json:
              schema: ErrorResponseModel
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                title: Response 401 Private Create Users Private Users Post
                type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                title: Response 403 Private Create Users Private Users Post
                type: string
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationError
    """
    if not check_user_is_admin():
        return return_error(403, "User is not admin")

    schema = PrivateCreateUserModelSchema()
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
            is_admin=values.get('is_admin'),
            city=values.get('city', None),
            additional_info=values.get('additional_info', None)
        )
        db.session.add(user)

    db.session.commit()
    result_schema = PrivateDetailUserResponseModelSchema()
    return result_schema.dump(user), 200
