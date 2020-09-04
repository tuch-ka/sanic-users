from sanic import Blueprint
from sanic.response import json, empty

from marshmallow import ValidationError
from schemas.user import UserAuthSchema
from models.user import User


bp = Blueprint('auth')


@bp.post('/auth')
async def login(request):
    """Авторизует пользователя и выдаёт ему JWT"""
    try:
        data = UserAuthSchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    user = await User.auth(data=data)

    if user is None:
        return empty(401)

    response = json({
        'user_id': user.user_id,
        'token': user.token
    }, status=200)
    response.cookies['token'] = user.token
    return response


@bp.post('/logout')
async def logout(request):
    """Отменяет авторизацию пользователя"""
    response = empty(200)
    del response.cookies['token']
    return response
