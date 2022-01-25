from flask import current_app
from app import get_current_db


db = get_current_db(current_app)


class City(db.Model):
    """
    Model for City table

    id: id of the city
    name: name of the city
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class User(db.Model):
    """
    Model for User table

    id: id of the user
    username: username
    password_hash: hash of user's password
    first_name: first name of the user
    last_name: last name of the user
    other_name: other name of the user
    email: user's email
    phone: user's phone
    birthday: user's date of birth
    is_admin: if user has admin rights
    additional_info: additional info of the user
    city: city of the user
    """

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
    """
    Creating a new user for table
    :return: new user
    """
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
