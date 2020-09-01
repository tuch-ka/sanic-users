from peewee import Model
from database import db


class BasicModel(Model):
    class Meta:
        database = db
