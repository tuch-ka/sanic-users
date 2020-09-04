import json
from unittest.mock import patch

import pytest

from app import create_app
from auth import create_token
from models.user import User


@pytest.yield_fixture
def app():
    application = create_app()
    yield application


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def returning_created_user(data) -> User:
    return User(**data)


async def returning_user_by_id(user_id) -> User:
    return User(user_id=user_id)


async def returning_none(data: None) -> None:
    return None


#########
# Tests #
#########


class TestUserRegistry(object):
    """
    POST /user/registry
    """

    async def test_user_registry_no_user_data(self, test_cli):
        """
        Регистрация пользователя c пустым запросом
        """
        user_data = dict()
        response = await test_cli.post('/user/registry', data=json.dumps(user_data))
        assert response.status == 400

    async def test_user_registry_no_password(self, test_cli):
        """
        Регистрация пользователя без указания пароля
        """
        user_data = {
            'username': 'testuser',
            'email': 'email@email.com',
        }
        response = await test_cli.post('/user/registry', data=json.dumps(user_data))
        assert response.status == 400

    async def test_user_registry_no_username(self, test_cli):
        """
        Регистрация пользователя без указания имени
        """
        user_data = {
            'password': 'password',
            'email': 'email@email.com',
        }
        response = await test_cli.post('/user/registry', data=json.dumps(user_data))
        assert response.status == 400

    @patch.object(User, 'create', returning_created_user)
    async def test_user_registry_good_data_with_flood(self, test_cli):
        """
        Регистрация пользователя с полными данными и лишним параметром
        """
        user_data = {
            'username': 'testuser',
            'password': 'password',
            'email': 'email@email.com',
            'foo': 'bar',
        }

        response = await test_cli.post('/user/registry', data=json.dumps(user_data))
        assert response.status == 201

        response_json = await response.json()
        assert user_data['username'] == response_json['username']
        assert user_data['email'] == response_json['email']
        assert 'foo' not in response_json

    @patch.object(User, 'create', returning_none)
    async def test_user_registry_duplicate_data(self, test_cli):
        """
        Регистрация пользователя с конфликтом имени
        """
        user_data = {
            'username': 'testuser',
            'password': 'password',
        }
        response = await test_cli.post('/user/registry', data=json.dumps(user_data))
        assert response.status == 409


class TestUserGet(object):
    """
    GET /user/<user_id>
    """
    cookies = {
        'token': create_token({'id': 0})
    }

    async def test_get_user_no_auth(self, test_cli):
        """
        Получение пользователя без авторизации
        """
        response = await test_cli.get(f'/user/{0}')
        assert response.status == 401

    @patch.object(User, 'get_by_id', returning_none)
    async def test_get_user_wrong_id(self, test_cli):
        """
        Получение пользователя с неверным id
        """
        response = await test_cli.get(f'/user/{0}', cookies=self.cookies)
        assert response.status == 404

    @patch.object(User, 'get_by_id', returning_user_by_id)
    async def test_get_user_wrong_id(self, test_cli):
        """
        Получение пользователя
        """
        response = await test_cli.get(f'/user/{0}', cookies=self.cookies)
        assert response.status == 200

        response_json = await response.json()
        assert response_json['user_id'] == 0
