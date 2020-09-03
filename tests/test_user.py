import asyncio
import json

import pytest

from app import create_app


@pytest.yield_fixture
def app():
    application = create_app()
    yield application


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


#########
# Tests #
#########


async def test_user_registry_no_password(test_cli):
    """
    POST /user/registry
    """
    user_data = {
        'username': 'testuser',
        'email': 'email@email.com',
    }
    response = await test_cli.post('/user/registry', data=json.dumps(user_data))
    assert response.status == 400


async def test_user_registry_no_username(test_cli):
    """
    POST /user/registry
    """
    user_data = {
        'password': 'password',
        'email': 'email@email.com',
    }
    response = await test_cli.post('/user/registry', data=json.dumps(user_data))
    assert response.status == 400


async def test_user_registry_good_data_with_flood(test_cli):
    """
    POST /user/registry
    """
    user_data = {
        'username': 'testuser',
        'password': 'password',
        'email': 'email@email.com',
        'foo': 'bar',
    }

    response = await test_cli.post('/user/registry', data=json.dumps(user_data))
    assert response.status == 201 or response.status == 409

    if response.status == 201:
        response_json = await response.json()
        assert user_data['username'] == response_json['username']
        assert user_data['email'] == response_json['email']
        assert 'foo' not in response_json


async def test_user_get_by_id_no_auth(test_cli):
    """
    GET /user/<user_id>
    """
    response = await test_cli.get(f'/user/{0}')
    assert response.status == 401
