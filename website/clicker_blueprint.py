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


def do_passive_income(seconds):
    db_sess = create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.money += user.passive_income_money * int(seconds)
    user.money_total += user.passive_income_money * int(seconds)
    user.experience += user.passive_income_exp * int(seconds)
    user.experience_total += user.passive_income_exp * int(seconds)
    db_sess.commit()


@clicker_blueprint.route('/start_page')
def start_page():
    db_sess = create_session()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        seconds = (dt.datetime.now() - user.last_time).seconds
        do_passive_income(seconds)
        user.last_time =dt.datetime.now()
        db_sess.commit()
        clicks_count = session.get('clicks_count', 0)
        return render_template('clicker.html', title='click', clicks_count=clicks_count)
    users = db_sess.query(User).all()
    return render_template('leader_board.html', users=users, title='leader_board')


@clicker_blueprint.route('/background_process_test')
def background_process_test():
    clicks_count = session.get('clicks_count', 0)
    session['clicks_count'] = clicks_count + 1
    return render_template('clicker.html', title='click', clicks_count=clicks_count)


@clicker_blueprint.route('/register', methods=['GET', 'POST'])
def reqister():
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
            return redirect("/start_page")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@clicker_blueprint.route('/profile')
def profile():
    db_sess = create_session()
    users = db_sess.query(User).all()
    return render_template('profile.html', users=users, title='profile')    
