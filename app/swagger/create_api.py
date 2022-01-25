from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from app.auth.schemas import auth_schemas
from app.users.schemas import user_schemas
from app.private.schemas import private_schemas
from app.common.schemas import common_schemas


def create_tags(spec):
    tags = [
        {'name': 'auth', 'description': "User's login and register"},
        {'name': 'private', 'description': "Admins part"},
        {'name': 'users', 'description': "User's part"}
    ]

    for tag in tags:
        spec.tag(tag)


def load_docstrings(spec, app):
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def delete_schema_in_name(name: str):
    index = name.lower().find('schema')
    if index != -1:
        return name[:index]
    return name


def get_apispec(app):
    spec = APISpec(
        title="My App",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )
    schemas = auth_schemas + user_schemas + private_schemas + common_schemas

    for schema in schemas:
        spec.components.schema(delete_schema_in_name(schema.__name__), schema=schema)

    create_tags(spec)

    load_docstrings(spec, app)

    return spec


def write_yaml_file(spec: APISpec, ):
    with open('files/api.yaml', 'w') as file:
        file.write(spec.to_yaml())
