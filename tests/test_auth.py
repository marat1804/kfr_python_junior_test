from . import *


def test_simple_login_and_logout(client, create_users):
    resp = client.get('users/current')
    assert resp.status_code == 401

    resp = client.post('/login', json={
        "username": "user_0",
        "password": "Qwerty12345"
    })
    data = resp.json
    assert resp.status_code == 200
    assert 'access_token_cookie' in resp.headers.get_all('Set-Cookie')[0]
    assert len(resp.headers.get_all('Set-Cookie')[0]) > 80
    assert 'refresh_token_cookie' in resp.headers.get_all('Set-Cookie')[1]
    assert len(resp.headers.get_all('Set-Cookie')[1]) > 80
    assert data['email'] == 'email_0@gmail.com'
    assert data['first_name'] == 'User 0'
    assert data['last_name'] == 'User 0'
    assert data['is_admin']
    assert data['phone'] is None
    assert data['birthday'] is None
    assert data['other_name'] is None

    resp = client.get('users/current')
    assert resp.status_code == 200

    resp = client.post('/logout')
    assert resp.status_code == 200
    assert 'access_token_cookie' in resp.headers.get_all('Set-Cookie')[0]
    assert len(resp.headers.get_all('Set-Cookie')[0]) < 80
    assert 'refresh_token_cookie' in resp.headers.get_all('Set-Cookie')[1]
    assert len(resp.headers.get_all('Set-Cookie')[1]) < 80

    resp = client.get('users/current')
    assert resp.status_code == 401


def test_login_wrong_credentials(client, create_users):
    resp = client.post('/login', json={
        "username": "user_0",
        "password": "Qwerty123"
    })
    assert resp.status_code == 401


def test_login_validation_error(client, create_users):
    resp = client.post('/login', json={
        "username": "user_0",
        "password": "Qwerty123"*100
    })
    json = resp.json
    assert resp.status_code == 422
    assert json['detail'][0]['loc'] == 'password'
    assert json['detail'][0]['msg'] == 'Longer than maximum length 128.'
    assert json['detail'][0]['type'] == 'Longer than maximum length 128.'


def test_register(client, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'Qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com',
        'other_name': 'User 3'
    }
    resp = client.post('/register', json=test_user)
    json = resp.json
    assert resp.status_code == 201
    assert json['email'] == test_user['email']
    assert json['birthday'] is None
    assert json['first_name'] == test_user['first_name']
    assert json['last_name'] == test_user['last_name']
    assert json['other_name'] == test_user['last_name']
    assert not json['is_admin']
    assert json['phone'] is None

    from app.common.models import User
    assert len(User.query.all()) == 4


def test_register_username_exists(client, create_users):
    test_user = {
        'username': 'user_0',
        'password': 'Qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com'
    }
    resp = client.post('/register', json=test_user)
    assert resp.status_code == 409


def test_register_email_exists(client, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'Qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_0@gmail.com',
        'other_name': 'User 3'
    }
    resp = client.post('/register', json=test_user)
    assert resp.status_code == 409


def test_register_weak_password(client, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_0@gmail.com',
        'other_name': 'User 3'
    }
    resp = client.post('/register', json=test_user)
    assert resp.status_code == 400


def test_refresh_cookies(client_user, create_users):
    resp = client_user.post('/refresh')
    assert resp.status_code == 200
    assert 'access_token_cookie' in resp.headers.get_all('Set-Cookie')[0]
    assert len(resp.headers.get_all('Set-Cookie')[0]) > 80
    assert 'refresh_token_cookie' in resp.headers.get_all('Set-Cookie')[1]
    assert len(resp.headers.get_all('Set-Cookie')[1]) > 80
