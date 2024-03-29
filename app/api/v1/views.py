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
        # Get page
        page = request.args.get("page", default=1, type=int)
        logger.info(f"PAGE: {page}")

        # Instantiate service from factory
        svc = create_pitch_list_service()
        pitch_list = svc.get_pitch_list(page)

        counts = svc.get_message_type_counts()

        body = {"messages": pitch_list, "counts": sorted(counts, key=lambda x: x["count"], reverse=True)}
        response = {"status": 200, "message": f"Found {len(pitch_list)} pitch records!", "body": body}

        return jsonify(response)

    def post(self):
        # Read body
        body = request.get_json()

        # Instantiate service from factory
        svc = create_pitch_list_service()

        # Create pitch list
        data = [{"timestamp": record["timestamp"], "message_type_id": record["message_type_id"]} for record in body]

        result = svc.create_pitch_list(data)
        logger.debug(f"{result}")

        if result:
            response = {"status": 201, "message": f"Uploaded pitch data successfully!"}
        else:
            response = {"status": 500, "message": f"Upload of pitch data unsuccessful!"}

        return jsonify(response)
