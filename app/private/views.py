from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.common.model_schemas import UserSchema
from app.common.utils import db_get_one_or_none, db_get_all, return_error, check_user_is_admin
from app.common.models import User
from app.users.schemas import CurrentUserResponseModelSchema, RequestUsersInQuerySchema, ShortenUserInfo, \
    PatchUserPersonalInfoSchema, UpdateUserResponseModelSchema

private_mod = Blueprint('private', __name__, url_prefix='/private')


@private_mod.route('/users', methods=['GET'])
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
    if not check_user_is_admin():
        return return_error(403, "User is not admin")
    try:
        request_schema = RequestUsersInQuerySchema().load(request.args)
    except ValidationError as ex:
        return return_error(409, ex.messages)
    page = request_schema.get('page', None)
    size = request_schema.get('size', None)
    users = db_get_all(User)
    response = {
        "data": ShortenUserInfo(many=True).dump(users[(page - 1) * size:page * size]),
        "meta": {
            "pagination": {
                "total": len(users),
                "page": page,
                "size": size
            }  # TODO CITIES
        }
    }
    return response, 200


