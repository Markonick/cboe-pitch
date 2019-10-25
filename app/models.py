from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
from sqlalchemy.orm import relationship, backref


class MessageType(db.Model):
    __tablename__ = "message_type"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False, unique=False)

    def __init__(self, description=None):
        self.description = description

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    message_type_id = db.Column(db.Integer, db.ForeignKey("message_type.id"), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False, unique=False)
    message_type = relationship(MessageType, backref=backref('messages', uselist=True))

    def __init__(self, message_type_id=None, timestamp=None):
        self.message_type_id = message_type_id
        self.timestamp = timestamp

