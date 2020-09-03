import pytest
from sanic.response import empty

from app import create_app
from auth import create_token, read_token, auth_required


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

def test_token_create_and_read():
    """Test creating readable tokens"""
    # Success
    payload = {'id': 1}
    created_token = create_token(payload)
    read_out_token = read_token(created_token)
    assert read_out_token == payload


def test_read_token_empty():
    """Test read_token"""
    broken_token_1 = read_token('')
    assert broken_token_1 is None


def test_read_token_wrong():
    """Test read_token"""
    broken_token_2 = read_token(
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
    )
    assert broken_token_2 is None


async def test_auth_required_not_authorized():
    """Test auth_required wrapper"""

    @auth_required
    async def auth_testing(_):
        return empty(200)

    request = type('EmptyObject', (object,), {})()
    request.cookies = {}

    response = await auth_testing(request)
    assert response.status == 401


async def test_auth_required_authorized():
    """Test auth_required wrapper"""

    @auth_required
    async def auth_testing(_):
        return empty(200)

    request = type('EmptyObject', (object,), {})()
    request.cookies = {'token': create_token({'id': 1})}

    response = await auth_testing(request)
    assert response.status == 200


async def test_logout(test_cli):
    """
    POST /user/logout
    """
    response = await test_cli.post('/user/logout')
    assert response.status == 200

    token = response.cookies.get('token').value
    assert not token
