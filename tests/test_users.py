from . import *


def test_users_current_without_auth(client, create_users):
    resp = client.get('/users/current')
    assert resp.status_code == 401


def test_users_current_ok(client_user, create_users):
    resp = client_user.get('/users/current')
    assert resp.status_code == 200
    data = resp.json
    assert data['email'] == 'user@gmail.com'
    assert data['first_name'] == 'User'
    assert data['last_name'] == 'User'
    assert not data['is_admin']
    assert data['phone'] is None
    assert data['birthday'] is None
    assert data['other_name'] is None


def test_users_list_without_query(client_user, create_users):
    resp = client_user.get('/users')
    assert resp.status_code == 422

    resp = client_user.get('/users?page=1')
    assert resp.status_code == 422

    resp = client_user.get('/users?page=2&soze=1')
    assert resp.status_code == 422


def test_users_list_without_auth(client, create_users):
    resp = client.get('/users')
    assert resp.status_code == 401


def test_users_list_ok(client_user, create_users):
    resp = client_user.get('/users?page=1&size=2')
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


def test_users_profile_without_auth(client, create_users):
    resp = client.patch('/users/profile', json={})
    assert resp.status_code == 401


def test_users_profile_validation_error(client_user, create_users):
    new_data = {
        'first_name': 'Top User',
        'email': '111'
    }
    resp = client_user.patch('/users/profile', json=new_data)
    assert resp.status_code == 422


def test_users_profile_ok(client_user, create_users):
    new_data = {
        'first_name': 'Top User',
        'email': 'new_email@gmail.com'
    }
    resp = client_user.patch('/users/profile', json=new_data)
    assert resp.status_code == 200
    data = resp.json
    assert data['email'] == new_data['email']
    assert data['first_name'] == new_data['first_name']
