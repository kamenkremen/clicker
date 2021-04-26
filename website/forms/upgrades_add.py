from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UpgradeAddForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    money_price = IntegerField('Цена в деньгах')
    experience_price = IntegerField('Цена в опыте')
    active_income_money = IntegerField('Активный доход денег')
    passive_income_money = IntegerField('Пассивный доход денег в секунду')
    active_income_exp = IntegerField('Активный доход опыта')
    passive_income_exp = IntegerField('Пассивный доход опыта в секунду')
    requirements = IntegerField('Требования(общий счёт)')
    submit = SubmitField('Подтвердить')
