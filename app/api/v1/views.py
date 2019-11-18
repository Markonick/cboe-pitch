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

page_cache = {}

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

        if page in page_cache:
            pitch_list = page_cache[page]
            logger.debug(f"CACHED PAGE: {page}, TRUE")
        else:
            pitch_list = svc.get_pitch_list(page)
            logger.debug(f"CACHED PAGE: {page}, FALSE")
            page_cache[page] = pitch_list
        
        # Get count per message type
        counts = svc.get_message_type_counts()
        # Get current count of messages in message table
        current_count = svc.get_current_count()
        # Get total count of messages in message table
        total_count = svc.get_total_count()

        body = {"totalCount": total_count, "currentCount": current_count, "messages": pitch_list, "counts": sorted(counts, key=lambda x: x["count"], reverse=True)}
        response = {"status": 200, "message": f"Found {len(pitch_list)} pitch records!", "body": body}

        return jsonify(response)

    def post(self):
        # Read body
        body = request.get_json()

        # Instantiate service from factory
        svc = create_pitch_list_service()

        # Create pitch list
        data = [{"timestamp": record["timestamp"], "message_type_id": record["message_type_id"]} for record in body[0]]
        
        logger.debug(f'TOTAL LINES: {body[1]} {type(body[1])}')
        count_result = svc.create_total_count(body[1])
        result = svc.create_pitch_list(data)
        logger.debug(f"{result}")

        if result:
            response = {"status": 201, "message": f"Uploaded pitch data successfully!"}
        else:
            response = {"status": 500, "message": f"Upload of pitch data unsuccessful!"}

        return jsonify(response)