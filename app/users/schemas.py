from marshmallow import Schema, fields
import app.common.fields as common_fields


class CurrentUserResponseModelSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=True)
    birthday = fields.Date(required=True)
    is_admin = fields.Boolean(required=True)


class RequestUsersInQuerySchema(Schema):
    page = common_fields.PositiveNumber(required=True)
    size = common_fields.PositiveNumber(required=True)


class ShortenUserInfo(CurrentUserResponseModelSchema):
    class Meta:
        exclude = ['other_name', 'phone', 'birthday', 'is_admin']
    id = fields.Integer(required=True)


class PaginatedMetaDataModelSchema(Schema):
    total = fields.Integer(required=True)
    page = fields.Integer(required=True)
    size = fields.Integer(required=True)


class UsersListMetaDataModelSchema(Schema):
    pagination = fields.Nested(PaginatedMetaDataModelSchema, many=False, required=True)


class UsersListResponseModel(Schema):
    data = fields.Nested(ShortenUserInfo, many=True, required=True)
    meta = fields.Nested(UsersListMetaDataModelSchema, many=False, required=True)


class PatchUserPersonalInfoSchema(Schema):
    first_name = common_fields.CommonName()
    last_name = common_fields.CommonName()
    other_name = common_fields.CommonName()
    email = common_fields.Email()
    phone = common_fields.Phone()
    birthday = fields.Date()
