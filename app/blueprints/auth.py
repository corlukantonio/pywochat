import functools
from typing import Any

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from sqlalchemy import Row, TextClause
from sqlalchemy.sql import text
from werkzeug import Response
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.user import User


class Auth:
    '''
    Auth.
    '''

    def register(self) -> Response | str:
        '''
        Registers.

        Returns:
            Response | str: Response.
        '''

        if request.method == 'POST':
            firstname: str | None = request.form['firstname']
            lastname: str | None = request.form['lastname']
            username: str | None = request.form['username']
            password: str | None = request.form['password']

            error: str | None = self.__get_register_error_message(
                firstname, lastname, username, password)

            if error is None:
                self.__insert_user(firstname, lastname, username, password)

                return redirect(url_for('auth.login'))

            flash(error, 'error')

        return render_template('auth/register.html')

    def __get_register_error_message(
            self,
            firstname: str,
            lastname: str,
            username: str,
            password: str) -> str | None:
        '''
        Gets register error message.

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
        elif self.__get_user_id_by_username(username) is not None:
            return f'User {username} is already registered.'

        return None

    def __get_user_id_by_username(self, username: str) -> Row[Any] | None:
        '''
        Gets user ID by username.

        Parameters:
            username (str): Username.

        Returns:
            Row[Any] | None: User ID.
        '''

        sql: TextClause = text(
            f'''
            SELECT id
            FROM {User.__tablename__}
            WHERE username = :username
            ''')
        params: dict[str, Any] = {'username': username}

        return db.session.execute(sql, params).fetchone()

    def __insert_user(self, firstname: str, lastname: str, username: str, password: str) -> None:
        '''
        Inserts user.

        Parameters:
            firstname (str): First name.
            lastname (str): Last name.
            username (str): Username.
            password (str): Password.
        '''

        sql: TextClause = text(
            f'''
            INSERT INTO {User.__tablename__} (username, password, firstname, lastname)
            VALUES (:username, :password, :firstname, :lastname)
            ''')
        params: dict[str, Any] = {
            'username': username,
            'password': generate_password_hash(password),
            'firstname': firstname,
            'lastname': lastname
        }

        db.session.execute(sql, params)
        db.session.commit()

    def login(self) -> Response | str:
        '''
        Logs in.

        Returns:
            Response | str: Response.
        '''

        if request.method == 'POST':
            username: str | None = request.form['username']
            password: str | None = request.form['password']

            user: Row[Any] | None = self.__get_user_by_username(username)

            error: str | None = self.__get_login_error_message(user, password)

            if error is None:
                session.clear()

                if user is not None:
                    session['user_id'] = user[0]

                return redirect(url_for('index'))

            flash(error)

        return render_template('auth/login.html')

    def __get_login_error_message(self, user: Row[Any] | None, password: str) -> str | None:
        '''
        Gets login error message.

        Parameters:
            user (Row[Any] | None): User.
            password (str): Password.

        Returns:
            str | None: Error message.
        '''

        if user is None:
            return 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            return 'Incorrect password.'

        return None

    def __get_user_by_username(self, username: str) -> Row[Any] | None:
        '''
        Gets user by username.

        Parameters:
            username (str): Username.

        Returns:
            Row[Any] | None: User ID.
        '''

        sql: TextClause = text(
            f'''
            SELECT *
            FROM {User.__tablename__}
            WHERE username = :username
            ''')
        params: dict[str, Any] = {'username': username}

        return db.session.execute(sql, params).fetchone()

    def logout(self) -> Response:
        '''
        Logout.

        Returns:
            Response: Response.
        '''

        session.clear()

        return redirect(url_for('index'))

    def load_logged_in_user(self) -> None:
        '''
        Loads logged in user.
        '''

        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            sql: TextClause = text(
                f'''
                SELECT *
                FROM {User.__tablename__}
                WHERE id = :id
                ''')
            params: dict[str, Any] = {'id': user_id}
            g.user = db.session.execute(sql, params).fetchone()


bp: Blueprint = Blueprint('auth', __name__, url_prefix='/auth')
auth: Auth = Auth()


@bp.route('/register', methods=('GET', 'POST'))
def register() -> Response | str:
    '''
    Registers.

    Returns:
        Response | str: Response.
    '''

    return auth.register()


@bp.route('/login', methods=('GET', 'POST'))
def login() -> Response | str:
    '''
    Logs in.

    Returns:
        Response | str: Response.
    '''

    return auth.login()


@bp.route('/logout')
def logout() -> Response:
    '''
    Logs out.

    Returns:
        Response: Response.
    '''

    return auth.logout()


@bp.before_app_request
def load_logged_in_user() -> None:
    '''
    Loads logged in user.
    '''

    auth.load_logged_in_user()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
