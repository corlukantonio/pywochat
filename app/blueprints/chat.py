from typing import Any, Sequence

from flask import Blueprint, render_template, session
from sqlalchemy import Row, TextClause
from sqlalchemy.sql import text

from ..extensions import db
from ..models.contact import Contact
from ..models.message import Message
from ..models.user import User


class Chat:
    '''
    Chat.
    '''

    def index(self) -> str:
        '''
        Index.

        Returns:
            str: Rendered template.
        '''

        all_contacts: Sequence[Row[Any]] = self.__get_all_contacts()
        user_id: int | None = self.__get_user_id()
        current_user = self.__get_current_user_by_id(user_id)

        if current_user is not None:
            contacts: Sequence[Row[Any]] = self.__get_current_user_contacts_by_username(
                current_user[1])

            messages: Sequence[Row[Any]] = self.__get_current_user_messages_by_id(
                current_user[0])

            return render_template(
                'chat/index.html', search_results_contacts=all_contacts, my_contacts=contacts, messages=messages)

        else:
            return render_template('chat/index.html', search_results_contacts=all_contacts)

    def __get_all_contacts(self) -> Sequence[Row[Any]]:
        '''
        Gets all contacts.

        Returns:
            Sequence[Row[Any]]: Contacts.
        '''

        sql: TextClause = text(
            f'''
            SELECT username, firstname, lastname
            FROM {User.__tablename__}
            ORDER BY username
            ''')

        return db.session.execute(sql).fetchall()

    def __get_user_id(self) -> int | None:
        '''
        Gets user ID.

        Returns:
            int | None: User ID.
        '''

        user_id = session.get('user_id')

        if user_id is None:
            return None

        try:
            return int(user_id)

        except ValueError:
            return None

    def __get_current_user_by_id(self, user_id: int | None) -> Row[Any] | None:
        '''
        Gets current user by ID.

        Parameters:
            user_id (int | None): ID.

        Returns:
            Row[Any] | None: User.
        '''

        if user_id is None:
            return None

        sql: TextClause = text(
            f'''
            SELECT id, username, password, firstname, lastname
            FROM {User.__tablename__}
            WHERE id = :user_id
            ''')
        params: dict[str, Any] = {'user_id': user_id}

        return db.session.execute(sql, params).fetchone()

    def __get_current_user_contacts_by_username(self, username: str) -> Sequence[Row[Any]]:
        '''
        Gets current user contacts by username.

        Parameters:
            username (str): Username.

        Returns:
            Sequence[Row[Any]]: Contacts.
        '''

        sql: TextClause = text(
            f'''
            SELECT DISTINCT u.firstname, u.lastname, c.user_2
            FROM {User.__tablename__} u, {Contact.__tablename__} c
            WHERE u.username = c.user_2 AND c.user_1 = :user_1
            ''')
        params: dict[str, Any] = {'user_1': username}

        return db.session.execute(sql, params).fetchall()

    def __get_current_user_messages_by_id(self, id: int) -> Sequence[Row[Any]]:
        '''
        Gets current user messages by ID.

        Parameters:
            id (int): ID.

        Returns:
            Sequence[Row[Any]]: Messages.
        '''

        sql: TextClause = text(
            f'''
            SELECT m.created, m.content,
            (
                SELECT u.username
                FROM {User.__tablename__} u
                WHERE u.id = m.author_id
            ) AS username,
            (
                SELECT u.username
                FROM {User.__tablename__} u
                WHERE u.id = m.sent_to_id
            ) AS username_receiver
            FROM {Message.__tablename__} m
            WHERE m.author_id = :user_id
            OR m.sent_to_id = :user_id
            ''')
        params: dict[str, Any] = {'user_id': id}

        return db.session.execute(sql, params).fetchall()


bp: Blueprint = Blueprint('chat', __name__)
chat: Chat = Chat()


@bp.route('/')
def index() -> str:
    '''
    Index.
    '''

    return chat.index()
