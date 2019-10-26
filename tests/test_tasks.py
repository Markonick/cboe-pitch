import pytest
import os
import json
import datetime
import logging
from unittest.mock import Mock, patch
from pytest import raises
from celery.exceptions import Retry

from celery.tasks import upload_pitch_data

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("CELERY TASKS TESTING")


@patch("requests.post")
def test_pitch_data_upload_success(mock_post):
    mock_post.return_value.ok = True

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
