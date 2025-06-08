import pytest
from testcontainers.postgres import PostgresContainer

from app import create_app


@pytest.fixture()
def app():
    with PostgresContainer('postgres:17.5-alpine3.21') as container:
        connection_uri: str = container.get_connection_url()

        app = create_app(environment='testing', connection_uri=connection_uri)

        yield app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        return client
