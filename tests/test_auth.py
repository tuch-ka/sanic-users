import json
from unittest.mock import patch

import pytest
from sanic.response import empty

from app import create_app
from auth import create_token, read_token, auth_required
from models.user import User


@pytest.yield_fixture
def app():
    application = create_app()
    yield application


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def returning_user(data) -> User:
    return User(**data, user_id=0)


async def returning_none(data: None) -> None:
    return None


class EmptyRequest:
    cookies = {}


@auth_required
async def auth_testing(_):
    # Декорированная функция заглушка
    return empty(200)


#########
# Tests #
#########


class TestToken(object):
    """
    Тестирование функций создания и чтения токена
    """

    def test_token_create_and_read(self):
        """Создание и чтение валидного токена"""
        payload = {'id': 1}
        created_token = create_token(payload)
        read_out_token = read_token(created_token)
        assert read_out_token == payload

    def test_read_token_empty(self):
        """Чтения пустого токена"""
        broken_token_1 = read_token('')
        assert broken_token_1 is None

    def test_read_token_wrong(self):
        """Чтение произвольного токена"""
        broken_token_2 = read_token(
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
        )
        assert broken_token_2 is None


class TestAuthWrapper(object):
    """
    Тестирование декоратора проверки авторизации
    """

    async def test_auth_required_not_authorized(self):
        """Не авторизованный запрос"""
        request = EmptyRequest()

        response = await auth_testing(request)
        assert response.status == 401

    async def test_auth_required_authorized(self):
        """Авторизованный запрос"""
        request = EmptyRequest()
        request.cookies = {'token': create_token({'id': 1})}

        response = await auth_testing(request)
        assert response.status == 200


class TestAuthEndpoints(object):
    """
    Тестирование снятия и выдачи авторизации
    """

    async def test_logout(self, test_cli):
        """
        POST /user/logout
        """
        response = await test_cli.post('/user/logout')
        assert response.status == 200

        token = response.cookies.get('token').value
        assert not token

    @patch.object(User, 'auth', returning_user)
    async def test_login_good_user(self, test_cli):
        """
        Удачная авторизация
        POST user/auth
        """
        user_data = {
            'username': 'testuser',
            'password': 'password',
        }

        response = await test_cli.post('/user/auth', data=json.dumps(user_data))
        assert response.status == 200

        response_json = await response.json()
        assert response_json['user_id'] == 0

        response_payload = read_token(response_json['token'])
        assert response_payload['user_id'] == 0

        assert 'token' in response.cookies

    @patch.object(User, 'auth', returning_none)
    async def test_login_bad_user(self, test_cli):
        """
        Неверный логин/пароль
        POST user/auth
        """
        user_data = {
            'username': 'testuser',
            'password': 'password',
        }

        response = await test_cli.post('/user/auth', data=json.dumps(user_data))
        assert response.status == 400

    @patch.object(User, 'auth', returning_none)
    async def test_login_bad_data(self, test_cli):
        """
        Неправильный запрос
        POST user/auth
        """
        user_data = {
            'foo': 'bar',
        }

        response = await test_cli.post('/user/auth', data=json.dumps(user_data))
        assert response.status == 400

