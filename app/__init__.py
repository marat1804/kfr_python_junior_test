from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

from app.users.views import users_mod
from app.auth.views import auth_mod
app.register_blueprint(users_mod)
app.register_blueprint(auth_mod)

from app.users.models import User
db.create_all()
db.session.commit()

if __name__ == '__main__':
	app.run()
