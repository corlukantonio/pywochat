import pytest
from testcontainers.postgres import PostgresContainer

from app import create_app_test


@pytest.fixture()
def app():
    with PostgresContainer('postgres:17.5-alpine3.21') as container:
        app = create_app_test(container.get_connection_url())

        yield app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        return client
