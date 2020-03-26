import os
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db

bp = Blueprint('chat', __name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@bp.route('/')
def index():
    db = get_db()
    all_contacts = db.execute(
        'SELECT firstname, lastname, username'
        ' FROM users'
        ' ORDER BY username'
    ).fetchall()

    user_id = session.get('user_id')

    currentUser = get_db().execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()

    if user_id is None or currentUser is None:
        currentUser = None
    else:
        my_contacts = db.execute(
            'SELECT DISTINCT u.firstname, u.lastname, c.user_2'
            ' FROM users u, contacts c'
            ' WHERE u.username = c.user_2'
            ' AND c.user_1 = ?',
            (currentUser['username'],)
        ).fetchall()

        my_messages = db.execute(
            'SELECT m.created, m.content,'
            ' ('
            '   SELECT u.username'
            '   FROM users u'
            '   WHERE u.id = m.author_id'
            ' ) AS username,'
            ' ('
            '   SELECT u.username'
            '   FROM users u'
            '   WHERE u.id = m.sent_to_id'
            ' ) AS username_receiver'
            ' FROM messages m'
            ' WHERE m.author_id = ?'
            ' OR m.sent_to_id = ?',
            (currentUser['id'], currentUser['id'],)
        ).fetchall()

    if user_id and currentUser is not None:
        return render_template('chat/index.html', all_contacts=all_contacts, my_contacts=my_contacts, my_messages=my_messages)
    else:
        return render_template('chat/index.html', all_contacts=all_contacts)


@bp.route('/profile/<string:currentUsername>', methods=('GET', 'POST'))
@login_required
def profile(currentUsername):
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static\\profile_images')
        user_id = session.get('user_id')
        db = get_db()

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist('file'):
            filename = file.filename
            destination = '\\'.join([target, filename])
            file.save(destination)

        short_path = destination.split('\\')
        short_path = str(short_path[-2] + '/' + short_path[-1])

        db.execute(
            'UPDATE users SET picture = ? WHERE id = ?',
            (short_path, user_id)
        )
        db.commit()

        return redirect(url_for('chat.profile', currentUsername=g.user['username']))

    return render_template('chat/profile.html')
