import logging
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import psycopg2
import os

from app import db
from app.models import Message, MessageType


# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("REPO")

db_password = os.environ.get("POSTGRES_PASSWORD")
db_username = os.environ.get("POSTGRES_USER")
db_host = os.environ.get("POSTGRES_HOST")
db_name = os.environ.get("POSTGRES_DB")
db_port = os.environ.get("POSTGRES_PORT")


def get_connection(schema):
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_username,
        host=db_host,
        password=db_password,
        port=db_port,
        options=f"-c search_path={schema}",
    )
    return conn

class PitchListRepo:
    """
    Repository for handling Pitch list
    """

    def __init__(self, per_page=10):
        self.per_page = per_page

    def get_pitch_list(self, page=1):
        # pitch_list = (
        #     Message.query.join(MessageType.messages)
        #     .order_by(Message.timestamp.desc())
        #     .values(Message.timestamp, Message.id, MessageType.description)
        # )

        offset = (page - 1) * self.per_page
        start = offset
        end = offset + self.per_page

        with get_connection('public') as db_conn:
            with db_conn.cursor() as cur:
                query = f"""
                    SELECT me.id, mt.description, me.timestamp FROM message as me
                    JOIN message_type as mt
                    ON me.message_type_id = mt.id
                    ORDER BY me.id DESC
                    LIMIT {self.per_page}
                    OFFSET {offset}
                """
                cur.execute(query)

                results = cur.fetchall()

                result = []
                for message_id, description, timestamp in results:
                    result.append({"message_id": message_id, "description": description, "timestamp": timestamp})

        # return result[start:end]
        return result

    def get_total_count(self):
        with get_connection('public') as db_conn:
            with db_conn.cursor() as cur:
                query = "SELECT count(*) from message"
                cur.execute(query)

                total_count = cur.fetchone() 

        return total_count

    def get_message_type_counts(self):

        # t = db.session.query(MessageType).join(MessageType.messages).subquery("t")

        # results = db.session.query(t.c.description, func.count(t.c.description).label("count")).group_by(
        #     t.c.description
        # )
        with get_connection('public') as db_conn:
            with db_conn.cursor() as cur:
                query = f"""
                WITH counts as (
                    SELECT message_type_id, count(message_type_id) 
                    AS count 
                    FROM message
                    GROUP BY message_type_id
                )
                SELECT description, count 
                FROM counts 
                JOIN message_type
                ON message_type_id = message_type.id
                """
                cur.execute(query)

                results = cur.fetchall()
                result = []
                logger.debug(results)
                for description, count in results:
                    result.append({"message_type": description, "count": count})

        # return sorted(result, key=lambda x: x["count"], reverse=True)
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
