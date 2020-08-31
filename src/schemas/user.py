from marshmallow import fields

from . import BasicSchema


class UserRegistrySchema(BasicSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=False)


class UserAuthSchema(BasicSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
