import os

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('chat', __name__)


@bp.route('/')
def index():
    from app import get_db
    db = get_db()

    all_contacts = db.session.execute(
        "SELECT firstname, lastname, username FROM users ORDER BY username"
    ).fetchall()

    user_id = session.get('user_id')

    currentUser = db.session.execute(
        "SELECT * FROM users WHERE id = :id",
        {'id': user_id}
    ).fetchone()

    if user_id is None or currentUser is None:
        currentUser = None
    else:
        my_contacts = db.session.execute(
            "SELECT DISTINCT u.firstname, u.lastname, c.user_2 FROM users u, contacts c WHERE u.username = c.user_2 AND c.user_1 = :user_1",
            {'user_1': currentUser['username']}
        ).fetchall()

        my_messages = db.session.execute(
            """SELECT m.created, m.content,
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
             OR m.sent_to_id = :current_user_id""",
            {'current_user_id': currentUser['id']}
        ).fetchall()

    if user_id and currentUser is not None:
        return render_template('chat/index.html', all_contacts=all_contacts, my_contacts=my_contacts, my_messages=my_messages)
    else:
        return render_template('chat/index.html', all_contacts=all_contacts)
