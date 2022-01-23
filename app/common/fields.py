from marshmallow import fields, validate
import re


def _apply_validator(field, validator):
    class ApplyValidator(field):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.validators.insert(0, validator)
    return ApplyValidator


PHONE_REGEX = re.compile(r'\+[0-9]{10,17}$')

email_validator = validate.Length(max=64)
common_name_validator = validate.Length(max=64)
password_validator = validate.Length(max=128)
phone_validator = validate.And(validate.Length(max=32), validate.Regexp(PHONE_REGEX))
positive_number_validator = validate.Range(0)

Email = _apply_validator(fields.Email, email_validator)
CommonName = _apply_validator(fields.String, common_name_validator)
Password = _apply_validator(fields.String, password_validator)
Phone = _apply_validator(fields.String, phone_validator)
PositiveNumber = _apply_validator(fields.Integer, positive_number_validator)
