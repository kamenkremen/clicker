from flask_restful import reqparse
from datetime import datetime

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('hashed_password', required=True)
user_parser.add_argument('upgrades', default='', type=str)

upgrade_parser = reqparse.RequestParser()
upgrade_parser.add_argument('name', required=True)
upgrade_parser.add_argument('money_price', required=True, type=int)
upgrade_parser.add_argument('experience_price', required=True, type=int)
upgrade_parser.add_argument('active_income_money', required=True, type=int)
upgrade_parser.add_argument('passive_income_money', required=True, type=int)
upgrade_parser.add_argument('active_income_exp', required=True, type=int)
upgrade_parser.add_argument('passive_income_exp', required=True, type=int)
upgrade_parser.add_argument('requirements', required=True, type=int)