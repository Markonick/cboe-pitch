import pytest
import os
import json
import datetime
import logging
from unittest.mock import Mock, patch

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("TASKS TESTING")


def test_get_response_returns_expected_pitch_data(client, init_database):
    response = client.get("/api/v1/pitch/")
    json_data = json.loads(response.data)

    assert len(json_data["body"]["messages"]) == 3
    assert json_data["body"]["messages"][0]["timestamp"] == "12345698"
    assert json_data["body"]["messages"][0]["description"] == "MsgType2"

    assert json_data["body"]["messages"][1]["timestamp"] == "12345688"
    assert json_data["body"]["messages"][1]["description"] == "MsgType1"

    assert json_data["body"]["messages"][2]["timestamp"] == "12345678"
    assert json_data["body"]["messages"][2]["description"] == "MsgType1"



def create_pitch_json():
    body = [
        {"timestamp": "11111111", "message_type_id": 0},
        {"timestamp": "22222222", "message_type_id": 1},
        {"timestamp": "11110110", "message_type_id": 1},
    ]

    return body
