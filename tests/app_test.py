import logging
import os

import pytest
from testcontainers.postgres import PostgresContainer

from app import create_app_test

# class TestPostgresInteraction(unittest.TestCase):
#     def setUp(self):
#         self.postgres_container = PostgresContainer("postgres:latest")
#         self.postgres_container.start()

#         # Get connection details from the container
#         self.host = self.postgres_container.get_container_host_ip()
#         self.port = self.postgres_container.get_exposed_port(5432)
#         self.username = self.postgres_container.get_username()
#         self.password = self.postgres_container.get_password()
#         self.database = self.postgres_container.get_database_name()

#         # Create a connection to the PostgreSQL database
#         self.connection = psycopg2.connect(
#             host=self.host,
#             port=self.port,
#             user=self.username,
#             password=self.password,
#             database=self.database,
#         )

#     def tearDown(self):
#         # Clean up after the test
#         self.connection.close()
#         self.postgres_container.stop()

#         # Your test code here, interacting with the PostgreSQL database
#         cursor = self.connection.cursor()
#         cursor.execute("SELECT 1")
#         result = cursor.fetchone()
#         self.assertEqual(result, (1,))


# if __name__ == "__main__":
#     unittest.main()


# def test_method():
#     assert 5 == 5
# def test_postgres_interaction(self):

@pytest.fixture
def client():
    with PostgresContainer('postgres:latest') as container:
        connection_uri = container.get_connection_url()

        os.environ['SQLALCHEMY_DATABASE_URI'] = connection_uri
        os.environ['PYWOCHAT_DATABASE_URI'] = connection_uri

        app = create_app_test(connection_uri)
        app.config.update({
            "SQLALCHEMY_DATABASE_URI": connection_uri
        })
        with app.test_client() as client:
            yield client


def test_postgres_container(client):
    # response = client.get("/auth/login")
    response = client.post("/auth/register", data={
        "firstname": "Jan",
        "lastname": "Kerekesh",
        "username": "jkerekesh",
        "password": "123456"
    })

    assert response.status_code == 302
