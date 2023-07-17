from typing import Any, Sequence

from flask import (Blueprint, Flask, flash, g, redirect, render_template,
                   request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Row, TextClause
from sqlalchemy.sql import text

from extensions import db

bp: Blueprint = Blueprint('chat', __name__)


@bp.route('/')
def index():

    all_contacts: Sequence[Row[Any]] = __get_all_contacts(db)
    user_id = session.get('user_id')
    current_user = __get_current_user_by_id(db, user_id)

    if user_id is None or current_user is None:
        current_user = None
    else:
        my_contacts: Sequence[Row[Any]] = __get_current_user_contacts_by_username(
            db, current_user[1])

        my_messages: Sequence[Row[Any]] = __get_current_user_messages_by_id(db, current_user[0])

    if user_id and current_user is not None:
        return render_template(
            'chat/index.html', all_contacts=all_contacts, my_contacts=my_contacts, my_messages=my_messages)
    else:
        return render_template('chat/index.html', all_contacts=all_contacts)


def __get_all_contacts(db: SQLAlchemy) -> Sequence[Row[Any]]:
    '''
    Gets all contacts.

    Parameters:
        db (SQLAlchemy): Database.

    Returns:
        Sequence[Row[Any]]: Contacts.
    '''

    sql: TextClause = text("SELECT firstname, lastname, username FROM users ORDER BY username")

    return db.session.execute(sql).fetchall()


def __get_current_user_by_id(db: SQLAlchemy, id: int):
    '''
    Gets current user by ID.

    Parameters:
        db (SQLAlchemy): Database.
        id (int): ID.

    Returns:
        Row[Any] | None: User.
    '''

    sql: TextClause = text("SELECT * FROM users WHERE id = :id")

    return db.session.execute(sql, {'id': id}).fetchone()


def __get_current_user_contacts_by_username(db: SQLAlchemy, username: str) -> Sequence[Row[Any]]:
    '''
    Gets current user contacts by username.

    Parameters:
        db (SQLAlchemy): Database.
        username (str): Username.

    Returns:
        Sequence[Row[Any]]: Contacts.
    '''

    sql: TextClause = text(
        """
        SELECT DISTINCT u.firstname, u.lastname, c.user_2
        FROM users u, contacts c
        WHERE u.username = c.user_2 AND c.user_1 = :user_1
        """)

    return db.session.execute(sql, {'user_1': username}).fetchall()


def __get_current_user_messages_by_id(db: SQLAlchemy, id: int) -> Sequence[Row[Any]]:
    '''
    Gets current user messages by ID.

    Parameters:
        db (SQLAlchemy): Database.
        id (int): ID.

    Returns:
        Sequence[Row[Any]]: Messages.
    '''

    sql: TextClause = text(
        """
        SELECT m.created, m.content,
        (
            SELECT u.username
            FROM users u
            WHERE u.id = m.author_id
        ) AS username,
        (
            SELECT u.username
            FROM users u
            WHERE u.id = m.sent_to_id
        ) AS username_receiver
        FROM messages m
        WHERE m.author_id = :current_user_id
        OR m.sent_to_id = :current_user_id
        """)

    return db.session.execute(sql, {'current_user_id': id}).fetchall()
