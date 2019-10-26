import logging
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

from app import db
from app.models import Message, MessageType


# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("REPO")


class PitchListRepo:
    """
    Repository for handling Pitch list
    """

    def __init__(self):
        pass

    def get_pitch_list(self, page=1):
        per_page = 100
        pitch_list = (
            Message.query.join(MessageType.messages).order_by(Message.timestamp.desc())
            .values(Message.timestamp, Message.id, MessageType.description)
            # .paginate(page, per_page, error_out=False)
        )

        result = []
        for timestamp, message_id, description in pitch_list:

            result.append({"message_id": message_id, "description": description, "timestamp": timestamp})
        offset = (page-1)*per_page
        start = offset
        end = offset + per_page
        return result[start:end]

    def get_message_type_counts(self):

        t = db.session.query(MessageType).join(MessageType.messages).subquery("t")

        results = db.session.query(t.c.description, func.count(t.c.description).label("count")).group_by(
            t.c.description
        )

        result = []

        for description, count in set(results):

            result.append({"message_type": description, "count": count})

        return result

    def create_pitch_list(self, records):
        try:
            pitch_data = [Message(record["message_type_id"], record["timestamp"]) for record in records]

            db.session.bulk_save_objects(pitch_data)
            logger.debug(f"CREATE PITCH REPO: COMMITING TO DB")
            db.session.commit()
        except Exception as e:
            logger.debug(f"PITCH REPO EXCEPTION: In rollback")
            logger.debug(f"PITCH REPO EXCEPTION: {e}")
            db.session.rollback()

            return False

        return True
