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

