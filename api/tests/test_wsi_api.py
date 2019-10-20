import pytest
from wsi_api import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def app_client(app):
    client = app.test_client()
    return client


def test_hello_world_view(client):
    hello_world_response = client.get('/')
    assert hello_world_response.status_code == 200
