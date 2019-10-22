import json
import typing
import os
import logging
from flask import request, jsonify
from flask_restplus import Resource, Namespace

from app.factories import create_pitch_list_service

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("API")

api = Namespace("pitch", description="CBOE pitch data related operations")


@api.route("/pitch", strict_slashes=False)
class PitchList(Resource):
    """
    Endpoint that returns a serialised ordered list of pitch data items
    """

    def get(self):
        # Get pitch data
        svc = create_pitch_list_service()
        pitch_list = svc.get_pitch_list()
        body = []

        for pitch_record in pitch_list:
            record = {"message_type": pitch_record.message_type, "timestamp": pitch_record.timestamp}
            body.append(record)

        response = {"status": 200, "message": f"Found {len(pitch_list)} pitch records!", "body": body}

        return jsonify(response)

    def post(self):
        # Read body fields
        body = request.get_json()
        timestamp = body.get("timestamp")
        message_type = body.get("message_type")

        # Instantiate service from factory
        svc = create_pitch_list_service()

        # Create pitch list
        result = svc.create_pitch_list(timestamp, message_type)

        if result:
            response = {"status": 201, "message": f"Uploaded pitch data successfully!"}
        else:
            response = {"status": 500, "message": f"Upload of pitch data unsuccessful!"}

        return jsonify(response)
