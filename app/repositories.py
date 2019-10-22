import logging
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
from app.models import Message


# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("REPO")


class PitchListRepo:
    """
    Repository for handling Pitch list
    """

    def __init__(self):
        pass

    def get_pitch_list(self):
        pitch_list = Message.query.all()
        return pitch_list

    def create_pitch_list(self, message_type, timestamp):
        try:
            pitch_data = [Message(record["timestamp"], record["message_type"]) for record in records]
            db.session.bulk_save_objects(pitch_data)
            logger.debug(f"CREATE PITCH REPO: COMMITING TO DB")
            db.session.commit()
        except Exception as e:
            logger.debug(f"PITCH REPO EXCEPTION: In rollback")
            logger.debug(f"PITCH REPO EXCEPTION: {e}")
            db.session.rollback()

            return False

        return True
