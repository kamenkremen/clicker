from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UpgradeAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    money_price = IntegerField('Money price', validators=[DataRequired()])
    experience_price = IntegerField('Experience price', validators=[DataRequired()])
    active_income_money = IntegerField('Active income money', validators=[DataRequired()])
    passive_income_money = IntegerField('Passive income money', validators=[DataRequired()])
    active_income_exp = IntegerField('Active income experience', validators=[DataRequired()])
    passive_income_exp = IntegerField('Passive income experience', validators=[DataRequired()])
    requirements = IntegerField('Requirements', validators=[DataRequired()])
    submit = SubmitField('Submit')
