import pytest
import logging
from unittest.mock import Mock, patch

from app.services import PitchListService

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("SERVICES TESTING")

MESSAGES = [
    {"message_id": 1, "description": "MsgType1", "timestamp": "11111111"},
    {"message_id": 2, "description": "MsgType1", "timestamp": "33111111"},
    {"message_id": 3, "description": "MsgType2", "timestamp": "44111111"},
    {"message_id": 4, "description": "MsgType3", "timestamp": "11111113"},
]

COUNTS = [
    {"message_type": "abc", "count": 1},
    {"message_type": "def", "count": 44},
]

def test_that_get_pitch_list_service_returns_elements():
    repo = Mock()
    repo.get_pitch_list.return_value = MESSAGES

    svc = PitchListService(repo)
    result = svc.get_pitch_list()

    assert result == MESSAGES


def test_that_get_pitch_list_service_returns_counts():
    repo = Mock()
    repo.get_message_type_counts.return_value = COUNTS

    svc = PitchListService(repo)
    result = svc.get_message_type_counts()

    assert result == COUNTS
