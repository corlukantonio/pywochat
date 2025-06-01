import json

from extensions import socketio


def test_chat(client):
    register_data = {
        'username': 'Raphael',
        'firstname': 'Dias Belloli',
        'lastname': 'raphinha',
        'password': '123456'
    }
    login_data = {
        'username': register_data['username'],
        'password': register_data['password']
    }
    expected_status_code = 200
    expected_content_type = 'text/html; charset=utf-8'

    client.post('/auth/register', data=register_data)
    client.post('/auth/login', data=login_data)
    response = client.get('/')

    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}."
    assert response.content_type == expected_content_type, \
        f"Expected content type {expected_content_type}, but got {response.content_type}."


def test_chat_with_contacts(client):
    socketio_client = socketio.test_client(client.application)
    register_data = {
        'firstname': 'Raphael',
        'lastname': 'Dias Belloli',
        'username': 'raphinha',
        'password': '123456'
    }
    contact_data = {
        'firstname': 'Ansu',
        'lastname': 'Fati',
        'username': 'ansufati',
        'password': '123456'
    }
    login_data = {
        'username': register_data['username'],
        'password': register_data['password']
    }
    expected_status_code = 200
    expected_content_type = 'text/html; charset=utf-8'
    expected_contact = 'Ansu Fati (ansufati)'

    client.post('/auth/register', data=register_data)
    client.post('/auth/register', data=contact_data)
    client.post('/auth/login', data=login_data)
    socketio_client.emit('add_contact', {
        'loggedInUserUsername': register_data['username'],
        'foundContact': [
            contact_data['firstname'],
            contact_data['lastname'],
            contact_data['username']]
    })
    response = client.get('/')

    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}."
    assert response.content_type == expected_content_type, \
        f"Expected content type {expected_content_type}, but got {response.content_type}."
    assert expected_contact in response.get_data(as_text=True), \
        f"Expected contact '{expected_contact}' to be in response, " \
        f"but it was not found in the response data."


def test_message(client):
    socketio_client = socketio.test_client(client.application)
    register_data = {
        'firstname': 'Cristiano',
        'lastname': 'Ronaldo',
        'username': 'cristiano',
        'password': '123456'
    }
    contact_data = {
        'firstname': 'Dani',
        'lastname': 'Olmo',
        'username': 'daniolmo',
        'password': '123456'
    }
    login_data = {
        'username': register_data['username'],
        'password': register_data['password']
    }
    message = 'Croatia should have won the World Cup in 2018!'
    message_sender_username = register_data['username']
    message_receiver_user = {
        'firstname': contact_data['firstname'],
        'lastname': contact_data['lastname'],
        'username': contact_data['username']
    }
    expected_response = {
        'message': message,
        'sender': {
            'id': 1,
            'username': message_sender_username
        },
        'receiver': {
            'id': 2,
            'username': message_receiver_user['username']
        }
    }

    client.post('/auth/register', data=register_data)
    client.post('/auth/register', data=contact_data)
    client.post('/auth/login', data=login_data)
    socketio_client.emit('add_contact', {
        'loggedInUserUsername': register_data['username'],
        'foundContact': [
            contact_data['firstname'],
            contact_data['lastname'],
            contact_data['username']]
    })
    socketio_client.send({
        'message': message,
        'senderUsername': message_sender_username,
        'receiverUser': message_receiver_user})
    response = json.loads(socketio_client.get_received()[0]['args'])

    assert response == expected_response, \
        f"Expected response {expected_response}, but got {response}."
