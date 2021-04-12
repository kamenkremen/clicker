import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .. import database


class Upgrade(database, SerializerMixin, UserMixin):
    __tablename__ = 'upgrades'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    money_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    experience_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    active_income = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    passive_income = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    requirements = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    requirements_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)

    user = orm.relation('User')
