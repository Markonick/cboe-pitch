import pytest
import os
import json
import datetime
import logging
import pandas as pd
from unittest.mock import Mock, patch
from pytest import raises

from celery.tasks import upload_pitch_data, parse_row, parse_data_file, post_data, add_periodic_task

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("CELERY TASKS TESTING")


@patch("requests.post")
def test_pitch_data_upload_success(mock_post):
    pass


def test_parse_row_returns_expected_result():
    row = "S28800011AAK27GA0000DTS000100SH"

    output = parse_row(row)

    assert output["timestamp"] == "28800011"
    assert output["message_type_id"] == 0


def create_pitch_json():
    body = [
        {"timestamp": "11111111", "message_type_id": 0},
        {"timestamp": "22222222", "message_type_id": 1},
        {"timestamp": "11110110", "message_type_id": 1},
    ]

    return body
