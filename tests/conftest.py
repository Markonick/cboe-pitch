import pytest
import datetime

from app import create_app
from app import db
from app.models import Message, MessageType


@pytest.fixture(scope="function")
def client():
    app = create_app(config_class="config.TestingConfig")
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


@pytest.fixture(scope="function")
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    messageType1 = MessageType("MsgType1")
    messageType2 = MessageType("MsgType2")
    db.session.add(messageType1)
    db.session.add(messageType2)
    message1 = Message(messageType1.id, "12345678")
    message2 = Message(messageType1.id, "12345688")
    message3 = Message(messageType2.id, "12345698")
    messageType1.messages.extend([message1, message2])
    messageType2.messages.extend([message3])

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
