from . import db
from models.user import User


def create_tables():
    with db:
        db.create_tables([User, ])
