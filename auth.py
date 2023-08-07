import functools
from typing import Any

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from sqlalchemy import Row, TextClause
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname: str | None = request.form['firstname']
        lastname: str | None = request.form['lastname']
        username: str | None = request.form['username']
        password: str | None = request.form['password']

        error: str | None = __get_error_message(firstname, lastname, username, password)

        if error is None:
            __insert_user(firstname, lastname, username, password)

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


def __get_error_message(firstname: str, lastname: str, username: str, password: str) -> str | None:
    '''
    Gets error message.

    Parameters:
        firstname (str): First name.
        lastname (str): Last name.
        username (str): Username.
        password (str): Password.

    Returns:
        str | None: Error message.
    '''

    if not firstname:
        return 'First name is required.'
    elif not lastname:
        return 'Last name is required.'
    elif not username:
        return 'Username is required.'
    elif not password:
        return 'Password is required.'
    elif __get_user_id_by_username(username) is not None:
        return 'User {} is already registered.'.format(username)

    return None


def __get_user_id_by_username(username: str) -> Row[Any] | None:
    '''
    Gets user ID by username.

    Parameters:
        username (str): Username.

    Returns:
        Row[Any] | None: User ID.
    '''

    sql: TextClause = text('SELECT id FROM users WHERE username = :username')
    params: dict[str, Any] = {'username': username}

    return db.session.execute(sql, params).fetchone()


def __insert_user(firstname: str, lastname: str, username: str, password: str) -> None:
    '''
    Inserts user.

    Parameters:
        firstname (str): First name.
        lastname (str): Last name.
        username (str): Username.
        password (str): Password.

    Returns:
        str | None: Error message.
    '''

    sql: TextClause = text(
        """
        INSERT INTO users (username, password, firstname, lastname)
        VALUES (:username, :password, :firstname, :lastname)
        """)
    params: dict[str, Any] = {
        'username': username,
        'password': generate_password_hash(password),
        'firstname': firstname,
        'lastname': lastname
    }

    db.session.execute(sql, params)
    db.session.commit()


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
