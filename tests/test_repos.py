import pytest
import os
import json
import datetime
import logging
from unittest.mock import patch

from app.models import Message, MessageType
from app.repositories import PitchListRepo

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("REPOS TESTING")


def test_that_get_pitch_list_repo_returns_list_of_message_dicts(client, init_database):
    per_page = 10
    repo = PitchListRepo(per_page)

    current_page = 1
    messages = repo.get_pitch_list(current_page)

    assert len(messages) == 3
    assert messages[0] == {"message_id": 3, "timestamp": "12345698", "description": "MsgType2"}
    assert messages[1] == {"message_id": 2, "timestamp": "12345688", "description": "MsgType1"}
    assert messages[2] == {"message_id": 1, "timestamp": "12345678", "description": "MsgType1"}


def test_that_get_pitch_list_repo_returns_only_1_message_when_repo_per_page_is_set_to_1(client, init_database):
    per_page = 1
    repo = PitchListRepo(per_page)

    current_page = 1
    messages = repo.get_pitch_list(current_page)
    assert len(messages) == 1


def test_that_get_pitch_list_repo_returns_only_2_message_when_repo_per_page_is_set_to_2(client, init_database):
    per_page = 2
    repo = PitchListRepo(per_page)

    current_page = 1
    messages = repo.get_pitch_list(current_page)
    assert len(messages) == 2


def test_that_get_pitch_list_repo_returns_top_message_when_repo_per_page_is_set_to_1(client, init_database):
    per_page = 1
    repo = PitchListRepo(per_page)

    current_page = 1
    messages = repo.get_pitch_list(current_page)

    assert messages[0] == {"message_id": 3, "timestamp": "12345698", "description": "MsgType2"}


def test_that_get_pitch_list_repo_returns_top_message_on_page_2_when_current_page_is_set_to_2(client, init_database):
    per_page = 1
    repo = PitchListRepo(per_page)

    current_page = 2
    messages = repo.get_pitch_list(current_page)
    assert len(messages) == 1

    assert messages[0] == {"message_id": 2, "timestamp": "12345688", "description": "MsgType1"}


def test_that_get_pitch_list_repo_returns_list_of_counts(client, init_database):
    per_page = 10
    repo = PitchListRepo(per_page)

    counts = repo.get_message_type_counts()

    assert len(counts) == 2

    assert counts[1] == {"message_type": "MsgType2", "count": 1}
    assert counts[0] == {"message_type": "MsgType1", "count": 2}


def test_that_create_pitch_list_repo_returns_true(client, init_database):
    per_page = 10
    repo = PitchListRepo(per_page)

    msg1 = {"message_type_id": 0, "timestamp": "55555555"}
    msg2 = {"message_type_id": 1, "timestamp": "66666666"}
    result = repo.create_pitch_list([msg1, msg2])

    assert result == True


def test_that_create_pitch_list_repo_returns_false_when_non_nullable_message_type_id_is_null(client, init_database):
    per_page = 10
    repo = PitchListRepo(per_page)

    msg1 = {"message_type_id": None, "timestamp": ""}
    msg2 = {"message_type_id": 1, "timestamp": "66666666"}
    result = repo.create_pitch_list([msg1, msg2])

    assert result == False
