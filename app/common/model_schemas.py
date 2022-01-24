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
    is_admin = auto_field(column_name='is_admin')
    additional_info = auto_field(column_name='additional_info')
    city = auto_field(column_name='city')


class CitySchema(SQLAlchemySchema):
    class Meta:
        model = City
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', dump_only=True)
    name = auto_field(column_name='name')


model_schemas = [UserSchema, CitySchema]
