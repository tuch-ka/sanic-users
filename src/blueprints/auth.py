from sanic import Blueprint
from sanic.response import json, empty

from marshmallow import ValidationError
from schemas.user import UserAuthSchema


bp = Blueprint('auth')


@bp.post('/auth')
async def login(request):

    try:
        data = UserAuthSchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    response = json({'status': 'OK'}, status=200)
    response.cookies['token'] = 'token'
    return response


@bp.post('/logout')
async def logout(request):
    response = empty(200)
    del response.cookies['token']
    return response
