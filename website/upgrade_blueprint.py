import flask
from flask import Flask, render_template, redirect, request
from flask import make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from flask import session
from . import create_session
from .models.users import User
from .models.upgrades import Upgrade
from .templates import *
from .forms.upgrades_add import UpgradeAddForm

upgrade_blueprint = flask.Blueprint('upgrade_blueprint', __name__)


@upgrade_blueprint.route('/upgrades')
def upgrades():
    db_sess = create_session()
    upgrades = db_sess.query(Upgrade).all()
    return render_template('upgrades.html', upgrades=upgrades, title='Upgrades')


@upgrade_blueprint.route('/upgrades_add', methods=['GET', 'POST'])
def upgrades_add():
    form = UpgradeAddForm()
    if form.validate_on_submit():
        db_sess = create_session()
        if db_sess.query(Upgrade).filter(Upgrade.name == form.name.data).first():
            return render_template('upgrades_add.html', title='Upgrades_add', form=form,
                                   message="This upgrade already exists")
        upgrade = Upgrade(
            name=form.name.data,
            money_price=form.money_price.data,
            experience_price=form.experience_price.data,
            active_income=form.active_income.data,
            passive_income=form.passive_income.data,
            requirements=form.requirements.data,
            requirements_amount=form.requirements_amount.data,
        )
        db_sess.add(upgrade)
        db_sess.commit()
        return redirect('/upgrades')
    return render_template('upgrades_add.html', title='Upgrades_add', form=form)