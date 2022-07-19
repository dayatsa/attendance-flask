from marshmallow import Schema, fields, ValidationError

class ActivitySchema(Schema):
    activity = fields.String(required=True)
    description = fields.String(required=True)