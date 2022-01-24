from . import *


def test_empty_db(client, create_users):
    resp = client.post('/login', json={
        "username": "user_0",
        "password": "qwerty12345"
    })
    assert resp.status_code == 200

