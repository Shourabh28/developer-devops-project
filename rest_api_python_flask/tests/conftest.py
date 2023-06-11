import os
from app import Message
from app import app
from config import get_env_db_url
from app import Message
import pytest

@pytest.fixture(scope='module')
def new_message():
    message = Message('0000', '1111', '111111', '222222')
    return message

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    #DB_URL = 'postgresql://postgres:postgres@flask_msg_db:5432/postgres'

    get_env_db_url()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!