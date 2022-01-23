from marshmallow import Schema, fields
import app.fields as common_fields


class RegistrationSchema(Schema):
    username = common_fields.CommonName(required=True)
    password = common_fields.Password(required=True)
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=True)
    birthday = fields.Date(required=True)


class ErrorResponseModelSchema(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)


class CurrentUserResponseModelSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=True)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=True)
    birthday = fields.Date(required=True)
    is_admin = fields.Boolean(required=True)


class LoginModelSchema(Schema):
    username = common_fields.CommonName(required=True)
    password = common_fields.Password(required=True)
