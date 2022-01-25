import os
import tempfile

import pytest

from app import create_app
from config.config import Config


test_config = Config
test_config.TESTING = True
test_config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
app_testing = create_app(test_config)
app_testing.db.create_all()


@pytest.fixture
def client():
    with app_testing.test_client() as client:
        yield client
    with app_testing.app_context():
        app_testing.db.session.remove()
        app_testing.db.drop_all()
        app_testing.db.create_all()


@pytest.fixture
def add_user_and_admin():
    from app.common.utils import init_user
    from app import get_current_db
    from werkzeug.security import generate_password_hash
    db_ = get_current_db(app_testing)
    users = [init_user(
        username=f'admin',
        password_hash=generate_password_hash(f'Qwerty12345'),
        first_name=f'Admin',
        last_name=f'Admin',
        email=f'admin@gmail.com',
        phone=None,
        birthday=None,
        is_admin=True,
        city=1,
        other_name=None), init_user(
        username=f'user',
        password_hash=generate_password_hash(f'Qwerty12345'),
        first_name=f'User',
        last_name=f'User',
        email=f'user@gmail.com',
        phone=None,
        birthday=None,
        is_admin=False,
        city=2,
        other_name=None)]
    db_.session.add_all(users)
    db_.session.commit()
    yield users


@pytest.fixture
def client_admin(client, add_user_and_admin):
    client.post('/login', json={
        "login": "admin",
        "password": "Qwerty12345"
    })
    yield client


@pytest.fixture
def client_user(client, add_user_and_admin):
    client.post('/login', json={
        "login": "user",
        "password": "Qwerty12345"
    })
    yield client


@pytest.fixture
def create_cities():
    from app.common.models import City
    from app import get_current_db
    db_ = get_current_db(app_testing)
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
    db_ = get_current_db(app_testing)
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


