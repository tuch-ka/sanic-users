from sanic import Sanic

from database.init_db import create_tables

from blueprints import api


def create_app():
    app = Sanic(__name__)

    app.blueprint(api)

    create_tables()

    return app
