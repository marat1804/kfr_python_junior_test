from marshmallow import Schema, fields


class ErrorResponseModelSchema(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)
