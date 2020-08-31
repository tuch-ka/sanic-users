from sanic import Blueprint
from sanic.response import json, empty


bp = Blueprint('auth')


@bp.post('/auth')
async def login(request):
    response = json({'status': 'OK'}, status=200)
    response.cookies['token'] = 'token'
    return response


@bp.post('/logout')
async def logout(request):
    response = empty(200)
    del response.cookies['token']
    return response
