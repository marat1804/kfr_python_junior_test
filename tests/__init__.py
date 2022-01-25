import os
import tempfile

import pytest

from app import create_app
from config import Config


test_config = Config
test_config.TESTING = True
test_config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
test_app = create_app(test_config)
test_app.db.create_all()


@pytest.fixture
def client():
    with test_app.test_client() as client:
        yield client
    with test_app.app_context():
        test_app.db.session.remove()
        test_app.db.drop_all()
        test_app.db.create_all()


@pytest.fixture
def add_user_and_admin():
    from app.common.utils import init_user
    from app import get_current_db
    from werkzeug.security import generate_password_hash
    db_ = get_current_db(test_app)
    users = [init_user(
        username=f'admin',
        password_hash=generate_password_hash(f'Qwerty12345'),
        first_name=f'Admin',
        last_name=f'Admin',
        email=f'admin@gmail.com',
        phone=None,
        birthday=None,
        is_admin=True,
        city=0,
        other_name=None), init_user(
        username=f'user',
        password_hash=generate_password_hash(f'Qwerty12345'),
        first_name=f'User',
        last_name=f'User',
        email=f'user@gmail.com',
        phone=None,
        birthday=None,
        is_admin=False,
        city=1,
        other_name=None)]
    db_.session.add_all(users)
    db_.session.commit()
    yield users


@pytest.fixture
def client_admin(client, add_user_and_admin):
    client.post('/login', json={
        "username": "admin",
        "password": "Qwerty12345"
    })
    yield client


@pytest.fixture
def client_user(client, add_user_and_admin):
    client.post('/login', json={
        "username": "user",
        "password": "Qwerty12345"
    })
    yield client


@pytest.fixture
def create_cities():
    from app.common.models import City
    from app import get_current_db
    db_ = get_current_db(test_app)
    cities = [City(name='Москва'),
              City(name='Санкт-Петербург')]
    db_.session.add_all(cities)
    db_.session.commit()
    yield cities


@pytest.fixture
def create_users(create_cities):
    from app.common.utils import init_user
    from app import get_current_db
    from werkzeug.security import generate_password_hash
    db_ = get_current_db(test_app)
    users = [init_user(
        username=f'user_{i}',
        password_hash=generate_password_hash(f'Qwerty12345'),
        first_name=f'User {i}',
        last_name=f'User {i}',
        email=f'email_{i}@gmail.com',
        phone=None,
        birthday=None,
        is_admin=i == 0,
        city=None,
        other_name=None
    )
        for i in range(3)]
    db_.session.add_all(users)
    db_.session.commit()
    yield users


