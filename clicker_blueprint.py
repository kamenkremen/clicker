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
from .forms.login import LoginForm
from .forms.register import RegisterForm
import datetime as dt

clicker_blueprint = flask.Blueprint('clicker_blueprint', __name__)


def do_passive_income():
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
    session['money_count'] = 0
    session['exp_count'] = 0


@clicker_blueprint.route('/start_page')
def start_page():
    db_sess = create_session()
    if current_user.is_authenticated:
        income_update()
        do_passive_income()
        db_sess.merge(current_user)
        db_sess.commit()
        return render_template('clicker.html', title='click')
    users = db_sess.query(User).order_by(User.total.desc()).limit(100).all()
    return render_template('leader_board.html', users=users, title='leader_board')


@clicker_blueprint.route('/money_add')
def money_add():
    session['money_count'] += 1
    return 'nothing'


@clicker_blueprint.route('/exp_add')
def exp_add():
    session['exp_count'] += 1
    return 'nothing'


@clicker_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@clicker_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/start_page')


@clicker_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['money_count'] = 0
            session['exp_count'] = 0
            return redirect("/start_page")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@clicker_blueprint.route('/profile')
def profile():
    db_sess = create_session()
    do_passive_income()
    db_sess.merge(current_user)
    db_sess.commit()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template('profile.html', user=user, title='profile')    
