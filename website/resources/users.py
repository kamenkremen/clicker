from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from werkzeug.security import generate_password_hash

from ..models.users import User
from .parsers import user_parser

from .. import create_session


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def set_password(self, password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('username', 'email', 'modifed_date', 'money', 'experience', 'money_total',
                  'experience_total', 'upgrades', 'active_income', 'passive_income', 'hashed_password'))})

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
            only=('username', 'email', 'modifed_date', 'money', 'experience', 'money_total', 'experience_total',
                  'upgrades', 'active_income', 'passive_income', 'hashed_password')) for item in users]})

    def post(self):
        args = user_parser.parse_args()
        session = create_session()
        user = User(
            username=args['username'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password'])
        )
        id_upgrades = map(int, args['upgrades'].split(','))
        for id_upgrade in id_upgrades:
            user.upgrade.append(session.query(Upgrade).get(id_upgrade))
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
