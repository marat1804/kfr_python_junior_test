from flask import current_app
from app import get_current_db


db = get_current_db(current_app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    other_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    additional_info = db.Column(db.String, nullable=True)
    city = db.Column(db.Integer, db.ForeignKey(City.id), nullable=True)


def init_user(username, password_hash, first_name, last_name, other_name, email, phone,
              birthday, city, is_admin=False, additional_info=None):
    user = User(username=username,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                other_name=other_name,
                email=email,
                phone=phone,
                birthday=birthday,
                is_admin=is_admin,
                city=city,
                additional_info=additional_info)
    return user


if __name__ == '__main__':
    db.create_all()
