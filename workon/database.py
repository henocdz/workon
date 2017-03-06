import datetime

from peewee import Model, CharField, TextField, DateTimeField
from playhouse.sqlite_ext import SqliteExtDatabase


db = SqliteExtDatabase('workon.db')

class BaseModel(Model):
    class Meta:
        database = db


class Project(BaseModel):
    name = CharField(unique=True)
    path = TextField(unique=True)  # there can only be one project per path and viceversa
    created_date = DateTimeField(default=datetime.datetime.now)


def setup():
    db.connect()
    db.create_tables([Project])
