from sanic import Blueprint
from sanic.response import json, empty


bp = Blueprint('user')


@bp.post('/registry')
async def create_user(request):
    return empty(status=201)


@bp.get('/<user_id:int>')
async def read_user(request, user_id):
    return json(
        {
            'user_id': user_id,
        },
        status=200
    )
