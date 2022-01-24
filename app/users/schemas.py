from marshmallow import Schema, fields, EXCLUDE
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
    class Meta:
        unknown = EXCLUDE
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
    class Meta:
        unknown = EXCLUDE
    first_name = common_fields.CommonName(required=False)
    last_name = common_fields.CommonName(required=False)
    other_name = common_fields.CommonName(required=False)
    email = common_fields.Email(required=False)
    phone = common_fields.Phone(required=False)
    birthday = fields.Date(required=False)


class UpdateUserResponseModelSchema(Schema):
    id = fields.Integer(required=True)
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=True)
    birthday = fields.Date(required=True)


user_schemas = [CurrentUserResponseModelSchema, ShortenUserInfo, PaginatedMetaDataModelSchema,
                UsersListMetaDataModelSchema, UsersListResponseModel, PatchUserPersonalInfoSchema,
                UpdateUserResponseModelSchema]
