import os
import logging
import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.repositories import PitchListRepo

# Setup connection to DB
db_password = os.environ.get("POSTGRES_PASSWORD")
engine = create_engine(f"postgresql://postgres:{db_password}@cboe-db:5432/pitch")

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("SYSTEM TESTING")


def test_that_we_get_20000_message_table_entries():
    # Prepare query
    columns = """
        message.id,
        message.message_type_id,
        message.timestamp
    """
    query = f"select {columns} from message "
    df = pd.read_sql_query(query, engine)

    assert len(df.index) == 20000


def test_that_we_get_4_message_types_in_desc_order(client):
    response = requests.get("http://localhost:5000/api/v1/pitch", headers=None)
    logger.debug(f"API RESPONSE: {response}")
    if response.status_code == 200:
        messages = response.json()
        logger.debug(f"API RESPONSE: {messages}")
        counts = messages["body"]["counts"]

    assert len(counts) == 4

    assert counts[0] == {"message_type": "Add Order (Short)", "count": 10361}
    assert counts[1] == {"message_type": "Order Cancel", "count": 9592}
    assert counts[2] == {"message_type": "Trade (Short)", "count": 27}
    assert counts[3] == {"message_type": "Order Executed", "count": 20}

