import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from sqlalchemy import TextClause
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = None

        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        elif db.session.execute(
            "SELECT id FROM users WHERE username = :username",
            {'username': username}
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.session.execute(
                "INSERT INTO users (username, password, firstname, lastname) VALUES (:username, :password, :firstname, :lastname)",
                {
                    'username': username,
                    'password': generate_password_hash(password),
                    'firstname': firstname,
                    'lastname': lastname
                }
            )
            db.session.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        sql: TextClause = text("SELECT * FROM users WHERE username = :username")

        user = db.session.execute(sql, {'username': username}).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        sql: TextClause = text("SELECT * FROM users WHERE id = :id")
        g.user = db.session.execute(sql, {'id': user_id}).fetchone()


@bp.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
