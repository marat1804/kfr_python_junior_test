from . import *


def test_private_users_without_auth(client, create_users):
    resp = client.get('/private/users')
    assert resp.status_code == 401


def test_private_users_not_admin(client_user, create_users):
    resp = client_user.get('/private/users')
    assert resp.status_code == 403


def test_private_users_bad_query(client_admin, create_users):
    resp = client_admin.get('/private/users')
    assert resp.status_code == 422

    resp = client_admin.get('/private/users?page=1')
    assert resp.status_code == 422

    resp = client_admin.get('/private/users?page=2&soze=1')
    assert resp.status_code == 422


def test_private_users_ok(client_admin, create_users):
    resp = client_admin.get('/private/users?page=1&size=2')
    assert resp.status_code == 200
    data = resp.json
    assert len(data['data']) == 2
    assert 'email' in data['data'][0]
    assert 'id' in data['data'][0]
    assert 'first_name' in data['data'][0]
    assert 'last_name' in data['data'][0]
    assert data['meta']['pagination']['page'] == 1
    assert data['meta']['pagination']['size'] == 2
    assert data['meta']['pagination']['total'] == 5
    assert len(data['meta']['hint']['city']) == 2


def test_private_users_post_without_auth(client, create_users):
    resp = client.post('/private/users')
    assert resp.status_code == 401


def test_private_users_post_not_admin(client_user, create_users):
    resp = client_user.post('/private/users')
    assert resp.status_code == 403


def test_private_users_post_weak_password(client_admin, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com',
        'other_name': 'User 3',
        'is_admin': False
    }
    resp = client_admin.post('/private/users', json=test_user)
    assert resp.status_code == 400


def test_private_users_post_username_exists(client_admin, create_users):
    test_user = {
        'username': 'user_0',
        'password': 'Qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com',
        'other_name': 'User 3',
        'is_admin': False
    }
    resp = client_admin.post('/private/users', json=test_user)
    assert resp.status_code == 409


def test_private_users_post_validation_error(client_admin, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'qwerty12345',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com',
        'other_name': 'User 3'
    }
    resp = client_admin.post('/private/users', json=test_user)
    assert resp.status_code == 422


def test_private_users_post_ok(client_admin, create_users):
    test_user = {
        'username': 'user_3',
        'password': 'Qwerty12345',
        'first_name': f'User 3',
        'last_name': f'User 3',
        'email': f'email_3@gmail.com',
        'other_name': 'User 3',
        'is_admin': False
    }
    resp = client_admin.post('/private/users', json=test_user)
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
    assert len(User.query.all()) == 6


def test_private_users_get_info_without_auth(client, create_users):
    resp = client.get(f'/private/users/{1}')
    assert resp.status_code == 401


def test_private_users_get_info_not_admin(client_user, create_users):
    resp = client_user.get(f'/private/users/{1}')
    assert resp.status_code == 403


def test_private_users_get_info_not_found(client_admin, create_users):
    resp = client_admin.get(f'/private/users/{9}')
    assert resp.status_code == 404


def test_private_users_get_info_ok(client_admin, create_users):
    resp = client_admin.get(f'/private/users/{1}')
    assert resp.status_code == 200
    data = resp.json
    assert data['city'] == 1
    assert data['email'] == 'admin@gmail.com'
    assert data['first_name'] == 'Admin'
    assert data['last_name'] == 'Admin'
    assert data['id'] == 1
    assert data['phone'] is None
    assert data['username'] == 'admin'


def test_private_users_patch_info_without_auth(client, create_users):
    resp = client.patch(f'/private/users/{1}')
    assert resp.status_code == 401


def test_private_users_patch_info_not_admin(client_user, create_users):
    resp = client_user.patch(f'/private/users/{1}')
    assert resp.status_code == 403


def test_private_users_patch_info_not_found(client_admin, create_users):
    new_data = {
        'first_name': 'Top User',
        'email': 'new_email@gmail.com'
    }
    resp = client_admin.patch(f'/private/users/{9}', json=new_data)
    assert resp.status_code == 404


def test_private_users_patch_info_validation_error(client_admin, create_users):
    new_data = {
        'first_name': 'Top User',
        'email': '111'
    }
    resp = client_admin.patch(f'/private/users/{3}', json=new_data)
    assert resp.status_code == 422


def test_private_users_patch_info_ok(client_admin, create_users):
    new_data = {
        'first_name': 'Top User',
        'email': 'new_email@gmail.com'
    }
    resp = client_admin.patch(f'/private/users/{3}', json=new_data)
    assert resp.status_code == 200
    data = resp.json
    assert data['email'] == new_data['email']
    assert data['first_name'] == new_data['first_name']


def test_private_users_delete_without_auth(client, create_users):
    resp = client.delete(f'/private/users/{1}')
    assert resp.status_code == 401


def test_private_users_delete_not_admin(client_user, create_users):
    resp = client_user.delete(f'/private/users/{1}')
    assert resp.status_code == 403


def test_private_users_delete_not_found(client_admin, create_users):
    resp = client_admin.delete(f'/private/users/{9}')
    assert resp.status_code == 404


def test_private_users_delete_ok(client_admin, create_users):
    resp = client_admin.delete(f'/private/users/{3}')
    assert resp.status_code == 204
    from app.common.models import User
    assert len(User.query.all()) == 4
