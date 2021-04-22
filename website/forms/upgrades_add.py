from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UpgradeAddForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    money_price = IntegerField('Money price', validators=[DataRequired()])
    experience_price = IntegerField('Experience price', validators=[DataRequired()])
    active_income = IntegerField('Active income', validators=[DataRequired()])
    passive_income = IntegerField('Passive income', validators=[DataRequired()])
    requirements = IntegerField('Requirements', validators=[DataRequired()])
    requirements_amount = IntegerField('Requirements amount', validators=[DataRequired()])
    submit = SubmitField('Submit')
