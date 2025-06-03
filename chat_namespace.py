import datetime
import json
from typing import Any

from flask_socketio import Namespace, send
from sqlalchemy import Row, TextClause, text

from extensions import db
from models.contact import Contact
from models.message import Message


class ChatNamespace(Namespace):
    def on_add_contact(self, json: dict[str, Any]) -> None:
        '''
        Adds contact.

        Parameters:
            json (dict[str, Any]): JSON.
        '''

        sql: TextClause = text(
            f'''
            INSERT INTO {Contact.__tablename__} (user_1, user_2)
            VALUES (:user_1, :user_2)
            ''')

        logged_in_user_username = json['loggedInUserUsername']
        found_contact_username = json['foundContact'][2]

        insert_params_list: list[dict[str, Any]] = [
            {'user_1': found_contact_username, 'user_2': logged_in_user_username},
            {'user_1': logged_in_user_username, 'user_2': found_contact_username}]

        for insert_params in insert_params_list:
            db.session.execute(sql, insert_params)

        db.session.commit()

    def on_choose_contact(self, *json: Any) -> None:
        '''
        Chooses contact.

        Parameters:
            *json (tuple[Any]): JSON.
        '''

        # TODO: Implement choosing contact logic.
        print(json)

    def on_message(self, msg: dict[str, Any]) -> None:
        '''
        Handles message.

        Parameters:
            msg (dict[str, Any]): Message.
        '''

        message_content: str = msg['content']
        sender_username: str = msg['senderUsername']
        receiver_username: str = msg['receiverUser']['username']

        sender: Row[Any] | None = self.__get_user_by_username(sender_username)
        receiver: Row[Any] | None = self.__get_user_by_username(
            receiver_username)

        if sender is None:
            raise ValueError('Sender cannot be None.')

        if receiver is None:
            raise ValueError('Receiver cannot be None.')

        self.__insert_message(message_content, sender, receiver)

        data = self.__get_msg_update(message_content, sender, receiver)

        send(json.dumps(data), broadcast=True)

    def __get_user_by_username(self, username: str) -> (Row[Any] | None):
        '''
        Gets user by username.

        Parameters:
            username (str): Username.

        Returns:
            Row[Any] | None: User.
        '''

        sql: TextClause = text(
            'SELECT * FROM users WHERE username = :username')
        params: dict[str, Any] = {'username': username}

        return db.session.execute(sql, params).fetchone()

    def __insert_message(self, msg: str, sender: Row[Any], receiver: Row[Any]) -> None:
        '''
        Inserts message.

        Parameters:
            msg (str): Message.
            sender (Row[Any]): Sender.
            receiver (Row[Any]): Receiver.
        '''

        sql: TextClause = text(
            f'''
            INSERT INTO {Message.__tablename__} (author_id, sent_to_id, created, content)
            VALUES (:author_id, :sent_to_id, :created, :content)
            ''')
        params: dict[str, Any] = {
            'author_id': sender[0],
            'sent_to_id': receiver[0],
            'created': datetime.datetime.utcnow(),
            'content': msg
        }

        db.session.execute(sql, params)
        db.session.commit()

    def __get_msg_update(self, msg: str, sender: Row[Any], receiver: Row[Any]) -> dict[str, Any]:
        '''
        Gets message update.

        Parameters:
            msg (str): Message.
            sender (Row[Any]): Sender.
            receiver (Row[Any]): Receiver.

        Returns:
            dict[str, Any]: Message update.
        '''

        return {
            'message': msg,
            'sender': {
                'id': sender.id,
                'username': sender.username
            },
            'receiver': {
                'id': receiver.id,
                'username': receiver.username
            }
        }
