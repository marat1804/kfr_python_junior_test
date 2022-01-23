from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.utils import db_get_one_or_none
from app.users.models import User
from app.users.schemas import CurrentUserResponseModelSchema

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


@users_mod.route('/', methods=['GET'])
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
              schema:
                $ref: '#/components/schemas/UsersListResponseModel'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponseModel'
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
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
    """
    schema = WorkIdInQuerySchema().load(request.args)


