from marshmallow import (
    Schema,
    EXCLUDE,
)


class BasicSchema(Schema):
    class Meta:
        unknown = EXCLUDE
