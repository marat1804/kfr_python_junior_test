from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


def populate_cities(file, db_session):
    lines = open(file, encoding='utf-8').read().splitlines()
    from app.common.models import City
    cur_cities = City.query.all()
    if len(cur_cities) == 0:
        cities = [City(name=city.strip()) for city in lines]
        db_session.add_all(cities)
        db_session.commit()


def get_current_db(application):
    with application.app_context():
        return application.db


def create_app(config=Config):
    SWAGGER_URL = '/swagger-ui'
    API_URL = '/api'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'My App'
        }
    )

    app = Flask(__name__)
    app.config.from_object(config)
    with app.app_context():
        db = SQLAlchemy(app)
        jwt = JWTManager(app)
        ma = Marshmallow(app)
        app.db = db

        from app.users.views import users_mod
        from app.auth.views import auth_mod
        from app.private.views import private_mod

        app.register_blueprint(users_mod)
        app.register_blueprint(auth_mod)
        app.register_blueprint(private_mod)
        app.register_blueprint(swagger_ui_blueprint, use_prefix=SWAGGER_URL)
        if not config.TESTING:
            from app.common.models import User, City
            db.create_all()
            db.session.commit()
            populate_cities('cities.txt', db.session)

        @app.route('/api')
        def create_swagger_spec():
            from app.swagger.create_api import get_apispec, write_yaml_file
            import json
            specs = get_apispec(app)
            write_yaml_file(specs)
            return json.dumps(specs.to_dict()), 200

    return app


if __name__ == '__main__':
    app = create_app(Config)
    app.run()
