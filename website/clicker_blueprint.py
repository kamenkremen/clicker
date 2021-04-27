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
from .forms.search import SearchForm
import datetime as dt

clicker_blueprint = flask.Blueprint('clicker_blueprint', __name__)


def do_passive_income(user_id):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    seconds = (dt.datetime.now() - user.last_time).seconds
    user.money += user.passive_income_money * int(seconds)
    user.money_total += user.passive_income_money * int(seconds)
    user.experience += user.passive_income_exp * int(seconds)
    user.experience_total += user.passive_income_exp * int(seconds)
    user.total = user.experience_total + user.money_total
    user.last_time = dt.datetime.now()
    db_sess.commit()


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
    current_user.experience_total += session.get('exp_count', 0)
    current_user.money += session.get('money_count', 0)
    current_user.money_total += session.get('money_count', 0)
    current_user.total = current_user.experience_total + current_user.money_total
    session['money_count'] = 0
    session['exp_count'] = 0

@clicker_blueprint.route('/')
@clicker_blueprint.route('/start_page')
def start_page():
    db_sess = create_session()
    if current_user.is_authenticated:
        do_passive_income_fo_current_user()
        income_update()
        db_sess.merge(current_user)
        db_sess.commit()
        return render_template('clicker.html', title='click')
    db_sess = create_session()
    users = db_sess.query(User).order_by(User.total.desc()).limit(100).all()
    return render_template('leader_board.html', users=users, title='leader_board')


@clicker_blueprint.route('/money_add')
def money_add():
    session['money_count'] += current_user.active_income_money
    return 'nothing'


@clicker_blueprint.route('/exp_add')
def exp_add():
    session['exp_count'] += current_user.active_income_exp
    return 'nothing'


@clicker_blueprint.route('/profile/<user_id>')
def profile(user_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    do_passive_income(user_id)
    db_sess.commit()
    return render_template('profile.html', user=user, title='profile')


@clicker_blueprint.route('/find_user', methods=['GET', 'POST'])
def find_user():
    if not current_user.is_authenticated:
        return redirect('/login')
    db_sess = create_session()
    form = SearchForm()
    if form.validate_on_submit():
        username = form.username.data
        users = db_sess.query(User).filter(User.username.like(f'%{username}%')).all()
    else:
        users = db_sess.query(User).all()
    return render_template('find_users.html', users=users, form=form)


# @clicker_blueprint.route('/add_friend/<user_id>')
# def add_friend(user_id):
#     db_sess = create_session()
#     user = db_sess.query(User).filter(User.id == current_user.id).first()
#     user.friends.append(db_sess.query(User).get(user_id))
#     db_sess.commit()
#     return redirect('/start_page')
