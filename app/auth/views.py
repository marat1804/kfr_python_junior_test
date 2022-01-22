from flask import Blueprint, request
from app import db
from app.users.models import User, init_user, UserRoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.schemas import RegistrationSchema, CurrentUserResponseModelSchema
from marshmallow import ValidationError

auth_mod = Blueprint('auth', __name__, url_prefix='')


def get_username_case_insensitive(email):
    from sqlalchemy import func
    return User.query.filter(func.lower(User.username) == func.lower(email)).one_or_none()


@auth_mod.route('/login', methods=['POST'])
def all_users():
    return {"all": "ALL"}, 200


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
        return {
            'code': 409,
            'message': ex.messages
        }, 409

    username = values['username']
    password_hash = generate_password_hash(values['password'])

    existing_user = get_username_case_insensitive(username)
    if existing_user is not None:
        return {
                   'code': 409,
                   'message': "Username already in user"
               }, 409
    else:
        user = init_user(
            username=username,
            password_hash=password_hash,
            first_name=values['first_name'],
            last_name=values['last_name'],
            other_name=values['other_name'],
            email=values['email'],
            phone=values['phone'],
            birthday=values['birthday'],
            role=UserRoleEnum.participant
        )
        db.session.add(user)

    db.session.commit()
    result_schema = CurrentUserResponseModelSchema()
    return result_schema.dump(user), 200
