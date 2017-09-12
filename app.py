#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, g, redirect, session, flash
from flask_login import LoginManager, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:neha@localhost:5432/Expense_db'
app.debug = True
app.secret_key = "Neha"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Expense(db.Model):
    __tablename__ = 'expense_category'
    id = db.Column('table_id', db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    food = db.Column(db.Integer)
    accomodation = db.Column(db.Integer)
    entertainment = db.Column(db.Integer)
    grocery = db.Column(db.Integer)
    travel = db.Column(db.Integer)
    clothes = db.Column(db.Integer)
    total = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)

    def __init__(self, description, food, accomodation, entertainment, grocery, travel, clothes):
        self.description = self.check_empty(description)
        self.food = self.check_empty(food)
        self.accomodation = self.check_empty(accomodation)
        self.entertainment = self.check_empty(entertainment)
        self.grocery = self.check_empty(grocery)
        self.travel = self.check_empty(travel)
        self.clothes = self.check_empty(clothes)
        self.pub_date = datetime.utcnow()

    def check_empty(self, string):
        if string:
            return string
        return 0

@app.route('/register', methods=['GET', 'POST'])
def register():
    print request
    if request.method == 'POST':
        register_user = User(request.form['username'], request.form[
                             'email'], request.form['password'],)
        db.session.add(register_user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(
        username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/show_expense')
def show_expense():
    return render_template('show_expense.html',
        expense_category=Expense.query.order_by(Expense.pub_date.desc()).all()
    )

@app.route('/new_expense', methods=['GET', 'POST'])
def new_expense():
    if request.method == 'POST':
        expense_category = Expense(
            request.form['description'],
            request.form['food'],
            request.form['accomodation'],
            request.form['entertainment'],
            request.form['grocery'],
            request.form['travel'],
            request.form['clothes']
        )
        db.session.add(expense_category)
        db.session.commit()
        return redirect(url_for('show_expense'))
    return render_template('new_expense.html')


if __name__ == "__main__":
    app.run()
