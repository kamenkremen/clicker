from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from werkzeug.security import generate_password_hash

from ..models.users import User
from ..models.upgrades import Upgrade
from .parsers import user_parser

from .. import create_session


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def set_password(password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('username', 'email', 'money', 'experience', 'money_total',
                  'experience_total', 'active_income_money', 'active_income_exp', 'passive_income_money',
                  'passive_income_exp', 'total',  'hashed_password', 'last_time'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('username', 'email', 'money', 'experience', 'money_total',
                  'experience_total', 'active_income_money', 'active_income_exp', 'passive_income_money',
                  'passive_income_exp', 'total',  'hashed_password', 'last_time')) for item in users]})

    def post(self):
        args = user_parser.parse_args()
        session = create_session()
        user = User(
            username=args['username'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password'])
        )
        session.commit()
        return jsonify({'success': 'OK'})
