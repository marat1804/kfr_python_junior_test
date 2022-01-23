from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.common.model_schemas import UserSchema
from app.common.utils import db_get_one_or_none, db_get_all, return_error
from app.common.models import User
from app.users.schemas import CurrentUserResponseModelSchema, RequestUsersInQuerySchema, ShortenUserInfo, \
    PatchUserPersonalInfoSchema, UpdateUserResponseModelSchema

users_mod = Blueprint('users', __name__, url_prefix='/users')


@users_mod.route('/current', methods=['GET'])
@jwt_required()
def current_user_info():
    """
    Get info about current user
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CurrentUserResponseModelSchema
        '401':
          description: Unauthorized
    """
    result_schema = CurrentUserResponseModelSchema()
    user_id = get_jwt_identity()
    user = db_get_one_or_none(User, 'id', user_id)
    return result_schema.dump(user), 200


@users_mod.route('', methods=['GET'])
@jwt_required()
def get_user_list():
    """
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
              schema: UsersListResponseModel
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
    try:
        request_schema = RequestUsersInQuerySchema().load(request.args)
    except ValidationError as ex:
        return return_error(409, ex.messages)
    page = request_schema.get('page', None)
    size = request_schema.get('size', None)
    users = db_get_all(User)
    response = {
        "data": ShortenUserInfo(many=True).dump(users[(page - 1)*size:page*size]),
        "meta": {
            "pagination": {
                "total": len(users),
                "page": page,
                "size": size
            }
        }
    }
    return response, 200


@users_mod.route('/profile', methods=['PATCH'])
@jwt_required()
def patch_current_user_info():
    """
    Change current user info
    ---
    patch:
      requestBody:
        required: true
        content:
          application/json:
            schema: PatchUserPersonalInfoSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UpdateUserResponseModelSchema
        '401':
          description: Unauthorized
    """
    values = PatchUserPersonalInfoSchema().load(request.json)
    user_id = get_jwt_identity()
    user = db_get_one_or_none(User, 'id', user_id)
    UserSchema(load_instance=True).load(values, instance=user, session=db.session, partial=True)
    db.session.commit()
    return UpdateUserResponseModelSchema().dump(user), 200
