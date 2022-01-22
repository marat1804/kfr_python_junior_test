import enum
from app import db
from sqlalchemy.ext.hybrid import hybrid_property


class UserRoleEnum(enum.Enum):
    participant = 'Participant'
    admin = 'Admin'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    other_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    role = db.Column(db.Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.participant)

    @hybrid_property
    def is_admin(self):
        return self.role == UserRoleEnum.admin


def init_user(username, password_hash, first_name, last_name, other_name, email, phone,
              birthday, role=UserRoleEnum.participant):
    user = User(username=username,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                other_name=other_name,
                email=email,
                phone=phone,
                birthday=birthday,
                role=role)
    return user


if __name__ == '__main__':
    db.create_all()
