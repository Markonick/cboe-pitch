import pytest
import datetime
from freezegun import freeze_time

from app import create_app
from app import db
from app.models import Pitch


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
    with freeze_time("2019-09-15 12:00:00"):
        pitch1 = Pitch(username="nicomark", first_name="Nicolas", last_name="Markos", created=datetime.datetime.now())
        pitch2 = Pitch(username="speedster", first_name="Efi", last_name="Pappa", created=datetime.datetime.now())
    db.session.add(pitch1)
    db.session.add(pitch2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
