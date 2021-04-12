import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .. import database


class Connect(database, SerializerMixin, UserMixin):
    __tablename__ = 'connections'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('upgrades.id'))