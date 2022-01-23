from marshmallow import Schema, fields, EXCLUDE
import app.common.fields as common_fields
from app.common.model_schemas import CitySchema
from app.users.schemas import ShortenUserInfo, PaginatedMetaDataModelSchema


class PrivateCreateUserModelSchema(Schema):
    username = common_fields.CommonName(required=True)
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    is_admin = fields.Boolean(required=True)
    password = common_fields.Password(required=True)
    other_name = common_fields.CommonName(required=False)
    phone = common_fields.Phone(required=False)
    birthday = fields.Date(required=False)
    city = fields.Integer(required=False)
    additional_info = common_fields.LongName(required=False)


class PrivateDetailUserResponseModelSchema(Schema):
    id = fields.Integer(required=True)
    username = common_fields.CommonName(required=True)
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    is_admin = fields.Boolean(required=True)
    other_name = common_fields.CommonName(required=False)
    phone = common_fields.Phone(nullable=True)
    birthday = fields.Date(nullable=True)
    city = fields.Integer(nullable=True)
    additional_info = common_fields.LongName(nullable=True)


class PrivateShortenInfoModelSchema(ShortenUserInfo):
    city = fields.Integer(nullable=True)


class PrivateUsersListHintMetaModelSchema(Schema):
    city = fields.Nested(CitySchema, many=True, required=True)


class PrivateUsersListMetaDataModelSchema(Schema):
    pagination = fields.Nested(PaginatedMetaDataModelSchema, many=False, required=True)
    hint = fields.Nested(PrivateUsersListHintMetaModelSchema, many=False, required=True)


class PrivateUsersListResponseModelSchema(Schema):
    data = fields.Nested(PrivateShortenInfoModelSchema, many=True, required=True)
    meta = fields.Nested(PrivateUsersListMetaDataModelSchema, many=False, required=True)


class PrivateUpdateUserModelSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    first_name = common_fields.CommonName(required=False)
    last_name = common_fields.CommonName(required=False)
    other_name = common_fields.CommonName(required=False)
    email = common_fields.Email(required=False)
    phone = common_fields.Phone(required=False)
    birthday = fields.Date(required=False)
    city = fields.Integer(required=False)
    additional_info = common_fields.LongName(required=False)
    is_admin = fields.Boolean(required=False)
