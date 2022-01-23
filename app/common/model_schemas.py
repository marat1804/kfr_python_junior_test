from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField
from .models import *


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', dump_only=True)
    username = auto_field(column_name='username', dump_only=True)
    first_name = auto_field(column_name='first_name')
    last_name = auto_field(column_name='last_name')
    other_name = auto_field(column_name='other_name')
    email = auto_field(column_name='email')
    phone = auto_field(column_name='phone')
    birthday = auto_field(column_name='birthday')
    role = EnumField(UserRoleEnum, data_key='role', by_value=True)
