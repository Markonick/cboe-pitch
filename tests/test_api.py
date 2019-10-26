import pytest
import os
import json
import datetime
import logging
from unittest.mock import Mock, patch

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("API TESTING")

# GETs
def test_get_response_is_200(client, init_database):
    response = client.get("/api/v1/pitch/")
    assert response.status_code == 200


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


def test_get_response_returns_expected_counts(client, init_database):
    response = client.get("/api/v1/pitch/")
    json_data = json.loads(response.data)

    counts = json_data["body"]["counts"]

    assert counts[0]["count"] == 2
    assert counts[1]["count"] == 1


def test_get_response_returns_expected_messageTypes(client, init_database):
    response = client.get("/api/v1/pitch/")
    assert response.status_code == 200

    json_data = json.loads(response.data)
    counts = json_data["body"]["counts"]

    assert counts[0]["message_type"] == "MsgType1"
    assert counts[1]["message_type"] == "MsgType2"


def test_that_we_get_200_with_zero_records_when_maximum_pagenumber_violated(client, init_database):
    response = client.get(f"/api/v1/pitch?page=2")
    json_data = json.loads(response.data)

    assert response.status_code == 200
    json_data = json.loads(response.data)

    assert len(json_data["body"]["messages"]) == 0


# POSTs
def test_that_when_we_create_a_pitch_we_get_201(client, init_database):
    body = create_pitch_json()
    headers = {"Content-Type": "application/json"}
    response = client.post(f"/api/v1/pitch/", data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data["status"] == 201


def test_that_when_we_create_a_pitch_we_have_one_more_pitch_in_list(client, init_database):
    body = create_pitch_json()
    logger.debug(f'BODY LENGTH!!!!: {len(body)}')
    headers = {"Content-Type": "application/json"}
    response = client.post("/api/v1/pitch?page=1", data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data["status"] == 201

    response = client.get("/api/v1/pitch/")
    json_data = json.loads(response.data)
    logger.debug(f'BODY LENGTH AFTER POST!!!!: {len(json_data["body"]["messages"])}')


    assert len(json_data["body"]["messages"]) == 6


def test_that_when_we_create_a_pitch_fields_are_as_expected(client, init_database):
    body = create_pitch_json()
    headers = {"Content-Type": "application/json"}
    response = client.post("/api/v1/pitch/", data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data["status"] == 201

    response = client.get("/api/v1/pitch/")
    json_data = json.loads(response.data)

    assert json_data["body"]["messages"][0]["timestamp"] == "22222222"
    assert json_data["body"]["messages"][0]["description"] == "MsgType1"

    assert json_data["body"]["messages"][1]["timestamp"] == "12345698"
    assert json_data["body"]["messages"][1]["description"] == "MsgType2"

    assert json_data["body"]["messages"][2]["timestamp"] == "12345688"
    assert json_data["body"]["messages"][2]["description"] == "MsgType1"

    assert json_data["body"]["messages"][3]["timestamp"] == "12345678"
    assert json_data["body"]["messages"][3]["description"] == "MsgType1"

    assert json_data["body"]["messages"][4]["timestamp"] == "11111111"
    assert json_data["body"]["messages"][4]["description"] == "MsgType1"

    assert json_data["body"]["messages"][5]["timestamp"] == "11110110"
    assert json_data["body"]["messages"][5]["description"] == "MsgType2"


def test_that_when_we_create_a_pitch_counts_are_as_expected(client, init_database):
    body = create_pitch_json()
    headers = {"Content-Type": "application/json"}
    response = client.post("/api/v1/pitch/", data=json.dumps(body), headers=headers)
    json_data = json.loads(response.data)

    assert response.status_code == 200
    assert json_data["status"] == 201

    response = client.get("/api/v1/pitch/")
    json_data = json.loads(response.data)

    counts = json_data["body"]["counts"]

    assert counts[0]["count"] == 4
    assert counts[1]["count"] == 2


def create_pitch_json():
    body = [
        {"timestamp": "11111111", "message_type_id": 1},
        {"timestamp": "22222222", "message_type_id": 1},
        {"timestamp": "11110110", "message_type_id": 2},
    ]

    return body
