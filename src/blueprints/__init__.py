from sanic import Blueprint

from .user import bp as user_bp
from .auth import bp as auth_bp


api = Blueprint.group(user_bp, auth_bp, url_prefix='user')
