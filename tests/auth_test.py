def test_register_login_and_logout(client):
    register_data = {
        'firstname': 'Kobe',
        'lastname': 'Bryant',
        'username': 'kbryant',
        'password': '123456'
    }
    login_data = {
        'username': register_data['username'],
        'password': register_data['password']
    }
    expected_register_status_code = 302
    expected_register_content_type = 'text/html; charset=utf-8'
    expected_register_location = '/auth/login'
    expected_login_status_code = 302
    expected_login_content_type = 'text/html; charset=utf-8'
    expected_login_location = '/'
    expected_logout_status_code = 302
    expected_logout_content_type = 'text/html; charset=utf-8'
    expected_logout_location = '/'

    register_response = client.post('/auth/register', data=register_data)
    login_response = client.post(register_response.location, data=login_data)
    logout_response = client.get('/auth/logout')

    assert register_response.status_code == expected_register_status_code, \
        f"Expected status code {expected_register_status_code}, " \
        f"but got {register_response.status_code}."
    assert register_response.content_type == expected_register_content_type, \
        f"Expected content type {expected_register_content_type}, "\
        f"but got {register_response.content_type}."
    assert register_response.location == expected_register_location, \
        f"Expected redirect to {expected_register_location}, " \
        f"but got {register_response.location}."
    assert login_response.status_code == expected_login_status_code, \
        f"Expected status code {expected_login_status_code}, " \
        f"but got {login_response.status_code}."
    assert login_response.content_type == expected_login_content_type, \
        f"Expected content type {expected_login_content_type}, " \
        f"but got {login_response.content_type}."
    assert login_response.location == expected_login_location, \
        f"Expected redirect to {expected_login_location}, " \
        f"but got {login_response.location}."
    assert logout_response.status_code == expected_logout_status_code, \
        f"Expected status code {expected_logout_status_code}, " \
        f"but got {logout_response.status_code}."
    assert logout_response.content_type == expected_logout_content_type, \
        f"Expected content type {expected_logout_content_type}, " \
        f"but got {logout_response.content_type}."
    assert logout_response.location == expected_logout_location, \
        f"Expected redirect to {expected_logout_location}, "\
        f"but got {logout_response.location}."


def test_try_register_with_empty_username(client):
    register_data = {
        'firstname': 'Lamine',
        'lastname': 'Yamal',
        'username': '',
        'password': '123456'
    }
    expected_status_code = 200
    expected_content_type = 'text/html; charset=utf-8'
    expected_error_message = 'Username is required.'

    response = client.post('/auth/register', data=register_data)

    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}."
    assert response.content_type == expected_content_type, \
        f"Expected content type {expected_content_type}, but got {response.content_type}."
    assert expected_error_message in response.get_data(as_text=True), \
        f"Expected error message '{expected_error_message}' not found in response."


def test_try_register_with_existing_username(client):
    existing_register_data = {
        'firstname': 'Robert',
        'lastname': 'Lewandowski',
        'username': 'rlewandowski',
        'password': '123456'
    }
    new_register_data = {
        'firstname': 'Fake Robert',
        'lastname': 'Fake Lewandowski',
        'username': existing_register_data['username'],
        'password': '123456'
    }
    expected_status_code = 200
    expected_content_type = 'text/html; charset=utf-8'
    expected_error_message = f'User {new_register_data["username"]} is already registered.'

    client.post('/auth/register', data=existing_register_data)
    response = client.post('/auth/register', data=new_register_data)

    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}."
    assert response.content_type == expected_content_type, \
        f"Expected content type {expected_content_type}, but got {response.content_type}."
    assert expected_error_message in response.get_data(as_text=True), \
        f"Expected error message '{expected_error_message}' not found in response."


def test_try_login_with_incorrect_password(client):
    register_data = {
        'firstname': 'Pedro',
        'lastname': 'Gonzalez Lopez',
        'username': 'pgonzalezlopez',
        'password': '123456'
    }
    login_data = {
        'username': register_data['username'],
        'password': 'incorrectpassword'
    }
    expected_status_code = 200
    expected_content_type = 'text/html; charset=utf-8'
    expected_error_message = 'Incorrect password.'

    client.post('/auth/register', data=register_data)
    response = client.post('/auth/login', data=login_data)

    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, but got {response.status_code}."
    assert response.content_type == expected_content_type, \
        f"Expected content type {expected_content_type}, but got {response.content_type}."
    assert expected_error_message in response.get_data(as_text=True), \
        f"Expected error message '{expected_error_message}' not found in response."
