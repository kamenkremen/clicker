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
import datetime as dt

upgrade_blueprint = flask.Blueprint('upgrade_blueprint', __name__)


def do_passive_income_fo_current_user():
    seconds = (dt.datetime.now() - current_user.last_time).seconds
    current_user.money += current_user.passive_income_money * int(seconds)
    current_user.money_total += current_user.passive_income_money * int(seconds)
    current_user.experience += current_user.passive_income_exp * int(seconds)
    current_user.experience_total += current_user.passive_income_exp * int(seconds)
    current_user.total = current_user.experience_total + current_user.money_total
    current_user.last_time = dt.datetime.now()


def income_update():
    current_user.experience += session.get('exp_count', 0)
    current_user.money += session.get('money_count', 0)
    current_user.money_total += session.get('money_count', 0)
    current_user.experience_total += session.get('exp_count', 0)
    current_user.total = current_user.experience_total + current_user.money_total
    session['money_count'] = 0
    session['exp_count'] = 0


@upgrade_blueprint.route('/upgrades')
def upgrades():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = create_session()
    income_update()
    do_passive_income_fo_current_user()
    db_sess.merge(current_user)
    db_sess.commit()
    upgrades = db_sess.query(Upgrade).all()
    return render_template('upgrades.html', upgrades=upgrades, title='Upgrades', user=current_user)


@upgrade_blueprint.route('/upgrade_buy/<upgrade_id>')
def buy_upgrade(upgrade_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = create_session()
    # print(upgrade_id)
    upgrade = db_sess.query(Upgrade).filter(Upgrade.id == upgrade_id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.money < upgrade.money_price or user.experience < upgrade.experience_price:
        return redirect('/upgrades')
    user.active_income_money += upgrade.active_income_money
    user.active_income_exp += upgrade.active_income_exp
    user.passive_income_money += upgrade.passive_income_money
    user.passive_income_exp += upgrade.passive_income_exp
    user.money -= upgrade.money_price
    user.experience -= upgrade.experience_price
    user.upgrades.append(db_sess.query(Upgrade).get(upgrade.id))
    db_sess.commit()
    return redirect('/upgrades')

@upgrade_blueprint.route('/upgrades_add', methods=['GET', 'POST'])
def upgrades_add():
    if not current_user.is_authenticated:
        return redirect('/login')
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
            active_income_money=form.active_income_money.data,
            passive_income_money=form.passive_income_money.data,
            active_income_exp=form.active_income_money.data,
            passive_income_exp=form.passive_income_exp.data,
            requirements=form.requirements.data,
        )
        db_sess.add(upgrade)
        db_sess.commit()
        return redirect('/upgrades')
    return render_template('upgrades_add.html', title='Upgrades_add', form=form)