from marshmallow import Schema, fields, ValidationError

class AuthenticationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)