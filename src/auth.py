from functools import wraps
from typing import Optional

import jwt
from sanic.response import empty


TOKEN_KEY = 'secret_key'    # TODO: в .env


def auth_required(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):

        token = request.cookies.get('token', None)
        token_payload = read_token(token)

        if token is None or token_payload is None:
            response = empty(401)
        else:
            response = await func(request, *args, **kwargs)

        return response
    return wrapper


def create_token(payload: dict) -> str:
    return jwt.encode(payload, TOKEN_KEY).decode('utf-8')


def read_token(token) -> Optional[dict]:
    try:
        return jwt.decode(token, TOKEN_KEY)
    except jwt.exceptions.DecodeError:
        return None
