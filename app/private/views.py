from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app import db
from app.common.model_schemas import UserSchema, CitySchema
from app.common.utils import db_get_one_or_none, db_get_all, return_error, check_user_is_admin, \
    register_user
from app.common.models import User, City
from app.private.schemas import PrivateCreateUserModelSchema, PrivateDetailUserResponseModelSchema, \
    PrivateShortenInfoModelSchema, PrivateUpdateUserModelSchema
from app.users.schemas import RequestUsersInQuerySchema

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
    return register_user(values, db.session, PrivateDetailUserResponseModelSchema())


@private_mod.route('/users/<int:pk>', methods=['GET'])
@jwt_required()
def private_get_full_user_info(pk):
    """
    get:
      parameters:
        - required: true
          schema:
            title: Pk
            type: integer
          name: pk
          in: path
      responses:
        '200':
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
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                title: Response 404 Private Get User Private Users  Pk  Get
                type: string
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationError
    """
    if not check_user_is_admin():
        return return_error(403, "User is not admin")

    user = db_get_one_or_none(User, 'id', pk)
    if user is None:
        return return_error(404, f"User with id = {pk} not found")
    return PrivateDetailUserResponseModelSchema().dump(user), 200


@private_mod.route('/users/<int:pk>', methods=['DELETE'])
@jwt_required()
def private_delete_user_by_id(pk):
    """
    delete:
      parameters:
        - required: true
          schema:
            title: Pk
            type: integer
          name: pk
          in: path
      responses:
        '204':
          description: Successful Response
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                title: Response 401 Private Delete User Private Users  Pk  Delete
                type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                title: Response 403 Private Delete User Private Users  Pk  Delete
                type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                title: Response 404 Private Get User Private Users  Pk  Get
                type: string
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationError
    """
    if not check_user_is_admin():
        return return_error(403, "User is not admin")

    user = db_get_one_or_none(User, 'id', pk)
    if user is None:
        return return_error(404, f"User with id = {pk} not found")
    db.session.delete(user)
    db.session.commit()
    return {}, 204


@private_mod.route('/users/<int:pk>', methods=['PATCH'])
@jwt_required()
def private_patch_user_by_id(pk):
    """
    patch:
      parameters:
        - required: true
          schema:
            title: Pk
            type: integer
          name: pk
          in: path
      requestBody:
        content:
          application/json:
            schema: PrivateUpdateUserModelSchema
        required: true
      responses:
        '200':
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
                title: Response 401 Private Patch User Private Users  Pk  Patch
                type: string
        '403':
          description: Forbidden
          content:
            application/json:
              schema:
                title: Response 403 Private Patch User Private Users  Pk  Patch
                type: string
        '404':
          description: Not Found
          content:
            application/json:
              schema:
                title: Response 404 Private Patch User Private Users  Pk  Patch
                type: string
        '422':
          description: Validation Error
          content:
            application/json:
              schema: HTTPValidationError
    """
    if not check_user_is_admin():
        return return_error(403, "User is not admin")
    values = PrivateUpdateUserModelSchema().load(request.json)
    user = db_get_one_or_none(User, 'id', pk)
    UserSchema(load_instance=True).load(values, instance=user, session=db.session, partial=True)
    db.session.commit()
    return PrivateDetailUserResponseModelSchema().dump(user), 200
