import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import generate_password_hash, check_password_hash
from .. import database


class User(database, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    money = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    experience = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    money_total = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    experience_total = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    upgrades = sqlalchemy.Column(sqlalchemy.String, default='')
    active_income = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    passive_income = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


    upgrades = orm.relation("Upgrade", back_populates='user')

    # def __repr__(self):
    #     return f'<Colonist> {self.id} {self.surname} {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)