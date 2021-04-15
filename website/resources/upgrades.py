from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from ..models.upgrades import Upgrade
from .parsers import upgrade_parser

from .. import create_session


def abort_if_upgrade_not_found(upgrade_id):
    session = create_session()
    upgrade = session.query(upgrade).get(upgrade_id)
    if not upgrade:
        abort(404, message=f"Upgrade {upgrade_id} not found")


class UpgradeResource(Resource):
    def get(self, upgrade_id):
        abort_if_upgrade_not_found(upgrade_id)
        session = create_session()
        upgrade = session.query(Upgrade).get(upgrade_id)
        return jsonify({'upgrades': upgrade.to_dict(
            only=('name', 'money_price', 'experience_price', 'active_income', 'passive_income', 'requirements',
                  'requirements_amount'))})

    def delete(self, upgrade_id):
        abort_if_news_not_found(upgrade_id)
        session = create_session()
        upgrade = session.query(Upgrade).get(upgrade_id)
        session.delete(upgrade)
        session.commit()
        return jsonify({'success': 'OK'})


class UpgradeListResource(Resource):
    def get(self):
        session = create_session()
        upgrades = session.query(Upgrade).all()
        return jsonify({'upgrades': [item.to_dict(
            only=('name', 'money_price', 'experience_price', 'active_income', 'passive_income', 'requirements',
                  'requirements_amount')) for item in upgrades]})

    def post(self):
        args = upgrade_parser.parse_args()
        session = create_session()
        upgrade = upgrade(
            name=args['name'],
            money_price=args['money_price'],
            experience_price=args['experience_price'],
            active_income=args['active_income'],
            passive_income=args['passive_income'],
            requirements=args['requirements'],
            requirements_amount=args['requirements_amount']
        )
        session.add(upgrade)
        session.commit()
        return jsonify({'success': 'OK'})
