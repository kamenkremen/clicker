import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .. import database


association_table = sqlalchemy.Table(
    'association', database.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('upgrades', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('upgrades.id'))
)


class Upgrade(database, SerializerMixin, UserMixin):
    __tablename__ = 'upgrades'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    money_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    experience_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    active_income_money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    passive_income_money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    active_income_exp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    passive_income_exp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    requirements = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
