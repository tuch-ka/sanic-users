from sanic import Sanic

from blueprints import api


def create_app():
    app = Sanic(__name__)

    app.blueprint(api)

    return app
