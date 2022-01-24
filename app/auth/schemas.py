from marshmallow import Schema, fields
import app.common.fields as common_fields


class LoginModelSchema(Schema):
    username = common_fields.CommonName(required=True)
    password = common_fields.Password(required=True)


class RegistrationSchema(Schema):
    username = common_fields.CommonName(required=True)
    password = common_fields.Password(required=True)
    first_name = common_fields.CommonName(required=True)
    last_name = common_fields.CommonName(required=True)
    other_name = common_fields.CommonName(required=False)
    email = common_fields.Email(required=True)
    phone = common_fields.Phone(required=False)
    birthday = fields.Date(required=False)
    city = fields.Integer(required=False)
    additional_info = common_fields.LongName(required=False)


auth_schemas = [LoginModelSchema, RegistrationSchema]
