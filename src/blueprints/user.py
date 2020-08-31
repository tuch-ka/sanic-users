from sanic import Blueprint
from sanic.response import json, empty

from marshmallow import ValidationError
from schemas.user import UserRegistrySchema


bp = Blueprint('user')


@bp.post('/registry')
async def create_user(request):
    try:
        user = UserRegistrySchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    return json(user, status=201)


@bp.get('/<user_id:int>')
async def read_user(request, user_id):
    return json(
        {
            'user_id': user_id,
        },
        status=200
    )
