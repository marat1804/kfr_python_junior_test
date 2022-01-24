from marshmallow import Schema, fields


class ErrorResponseModelSchema(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)


class ValidationErrorSchema(Schema):
    loc = fields.String(required=True)
    msg = fields.String(required=True)
    type = fields.String(required=True)


class HTTPValidationErrorSchema(Schema):
    detail = fields.Nested(ValidationErrorSchema, many=False)


common_schemas = [ErrorResponseModelSchema, ValidationErrorSchema, HTTPValidationErrorSchema]
