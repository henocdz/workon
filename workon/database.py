import datetime
import os

from peewee import Model, CharField, TextField, DateTimeField
from playhouse.sqlite_ext import SqliteExtDatabase

from workon.helpers import get_project_path


db_path = os.path.join(get_project_path(), 'workon.db')
db = SqliteExtDatabase(db_path)

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
