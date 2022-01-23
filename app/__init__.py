from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


def populate_cities(file, db_session):
	lines = open(file, encoding='utf-8').read().splitlines()
	from app.common.models import City
	cur_cities = City.query.all()
	if len(cur_cities) == 0:
		cities = [City(name=city.strip()) for city in lines]
		db_session.add_all(cities)
		db_session.commit()


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)

from app.users.views import users_mod
from app.auth.views import auth_mod
from app.private.views import private_mod
app.register_blueprint(users_mod)
app.register_blueprint(auth_mod)
app.register_blueprint(private_mod)

from app.common.models import User, City
db.create_all()
db.session.commit()
populate_cities('cities.txt', db.session)

if __name__ == '__main__':
	app.run()
