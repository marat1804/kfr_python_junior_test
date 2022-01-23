from marshmallow import Schema, fields, EXCLUDE
import app.common.fields as common_fields
from app.common.model_schemas import CitySchema
from app.users.schemas import ShortenUserInfo, PaginatedMetaDataModelSchema


class PrivateCreateUserModelSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=True)
    birthday = fields.Date(required=True)
    is_admin = fields.Boolean(required=True)
    # TODO


class PrivateUsersListHintMetaModelSchema(Schema):
    city = fields.Nested(CitySchema, many=True, required=True)


class PrivateUsersListMetaDataModelSchema(Schema):
    pagination = fields.Nested(PaginatedMetaDataModelSchema, many=False, required=True)
    hint = fields.Nested(PrivateUsersListHintMetaModelSchema, many=False, required=True)


class PrivateUsersListResponseModelSchema(Schema):
    data = fields.Nested(ShortenUserInfo, many=True, required=True)
    meta = fields.Nested(PrivateUsersListMetaDataModelSchema, many=False, required=True)
