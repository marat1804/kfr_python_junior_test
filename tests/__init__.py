import os
import tempfile

import pytest


@pytest.fixture
def init_app():

    from app import create_app
    from config import Config
    test_config = Config
    test_config.TESTING = True
    test_config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # DATABASE = db_path

    # os.close(db_fd)
    # os.unlink(db_path)
    test_app = create_app(test_config)
    with test_app.app_context():
        yield test_app




@pytest.fixture
def client(init_app):
    with init_app.test_client() as client:
        yield client


@pytest.fixture
def create_users(init_app):
    from app.common.utils import init_user
    from app.common.models import User
    from app import get_current_db
    from werkzeug.security import generate_password_hash
    db_ = get_current_db(init_app)
    users = [init_user(
        username=f'user_{i}',
        password_hash=generate_password_hash(f'qwerty12345'),
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
    print("1 TUT", User.query.all())
    db_.session.add_all(users)
    db_.session.commit()
    print("2 TUT", User.query.all())
    yield init_app
