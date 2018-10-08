import os.path
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db

bp = Blueprint('chat', __name__)

@bp.route('/')
def index():
    db = get_db()
    all_contacts = db.execute(
        'SELECT firstname, lastname, username'
        ' FROM user'
        ' ORDER BY username'
    ).fetchall()

    user_id = session.get('user_id')

    if user_id is None:
        currentUser = None
    else:
        currentUser = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        my_contacts = db.execute(
            'SELECT DISTINCT u.firstname, u.lastname, c.user_2'
            ' FROM user u, contact c'
            ' WHERE u.username = c.user_2'
            ' AND c.user_1 = ?', (currentUser['username'],)
        ).fetchall()

        my_messages = db.execute(
            'SELECT m.created, m.content, (SELECT u.username FROM user u WHERE u.id = m.author_id) AS username, (SELECT u.username FROM user u WHERE u.id = m.sent_to_id) AS username_reciver'
            ' FROM message m'
            ' WHERE m.author_id = ? OR m.sent_to_id = ?', (currentUser['id'], currentUser['id'],)
        ).fetchall()

    if user_id:
        return render_template('chat/index.html', all_contacts = all_contacts, my_contacts = my_contacts, my_messages = my_messages)
    else:
        return render_template('chat/index.html', all_contacts = all_contacts)

@bp.route('/profile/<string:currentUsername>', methods=('GET', 'POST'))
@login_required
def profile(currentUsername):
    if request.method == 'POST':
        db = get_db()
        picture = request.form['picture']

        return redirect(url_for('chat.profile', currentUsername = g.user['username']))

    return render_template('chat/profile.html')
