from sanic import Sanic


def create_app():
    app = Sanic(__name__)

    return app
