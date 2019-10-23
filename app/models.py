from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message_type_id = db.Column(db.Integer, db.ForeignKey("message_types.id"), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, message_type_id=None, timestamp=None):
        self.message_type_id = message_type_id
        self.timestamp = timestamp


class MessageType(db.Model):
    __tablename__ = "message_types"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, description=None):
        self.description = description
