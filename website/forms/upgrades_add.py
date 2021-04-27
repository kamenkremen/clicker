from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UpgradeAddForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    money_price = IntegerField('Цена в деньгах', validators=[DataRequired()])
    experience_price = IntegerField('Цена в опыте', validators=[DataRequired()])
    active_income_money = IntegerField('Активный доход денег', validators=[DataRequired()])
    passive_income_money = IntegerField('Пассивный доход денег в секунду', validators=[DataRequired()])
    active_income_exp = IntegerField('Активный доход опыта', validators=[DataRequired()])
    passive_income_exp = IntegerField('Пассивный доход опыта в секунду', validators=[DataRequired()])
    requirements = IntegerField('Требования(общий счёт)', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
