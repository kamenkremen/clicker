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

clicker_blueprint = flask.Blueprint('clicker_blueprint', __name__)


@clicker_blueprint.route('/start_page')
def start_page():
    if current_user.is_authenticated:
        money_count = session.get('money_count', 0)
        exp_count = session.get('exp_count', 0)
        db_sess = create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.experience = exp_count
        user.money = money_count
        db_sess.commit()
        return render_template('clicker.html', title='click', money_count=money_count, exp_count=exp_count)
    db_sess = create_session()
    users = db_sess.query(User).all()
    return render_template('leader_board.html', users=users, title='leader_board')


@clicker_blueprint.route('/money_add')
def money_add():
    money_count = session.get('money_count', 0) + current_user.active_income_money
    session['money_count'] = money_count
    return 'nothing'


@clicker_blueprint.route('/exp_add')
def exp_add():
    exp_count = session.get('exp_count', 0) + current_user.active_income_exp
    session['exp_count'] = exp_count
    return 'nothing'


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
            session['money_count'] = current_user.money
            session['exp_count'] = current_user.experience
            return redirect("/start_page")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@clicker_blueprint.route('/profile')
def profile():
    db_sess = create_session()
    users = db_sess.query(User).all()
    return render_template('profile.html', users=users, title='profile')    
