import json
import os
import requests
from datetime import datetime
import random
import string
import logging
import glob
import pandas as pd
from celery import Celery
import pathlib

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("CELERY-TASKS")

# Get env vars
endpoint = os.environ.get("PITCH_ENDPOINT")
broker = os.environ.get("CELERY_BROKER_URL")
backend = os.environ.get("CELERY_RESULT_BACKEND")
datafile = os.environ.get("DATA_FILE")
basedir = os.path.abspath(os.path.dirname(__file__))
datafile_path = os.path.join(basedir, datafile)

celery = Celery(broker=broker, backend=backend)

# Add periodic tasks to scheduler
@celery.on_after_configure.connect
def add_periodic_task(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        upload_pitch_data,
        name="Upload new pitch data file every 10 sec, if there is a file available in the path",
    )


@celery.task
def upload_pitch_data():
    """
    START RUNNING
    =============
    find . -name "*.pyc" -exec rm -f {} \;
    sudo rm -rf migrations/
    docker exec -it backend flask db init
    docker exec -it backend flask db migrate
    docker exec -it backend flask db upgrade
    cp pitch_data.txt celery/
    """
    # Check if file in data file is in expected input path location
    path = pathlib.Path(datafile_path)
    if not path.exists():
        logger.debug(f"DATA FILE DOES NOT EXIST!!")
        return

    chunksize = 1000
    for chunk in pd.read_csv(
        datafile_path, chunksize=chunksize, delim_whitespace=True, header=None, names=["First", "Second"]
    ):
        parsed_pitch_data_df = parse_data_file(chunk)
        headers = {"Content-Type": "application/json"}
        body = parsed_pitch_data_df.tolist()

        data_json = json.dumps(body)
        response = requests.post(endpoint, data=data_json, headers=headers)
        logger.debug(f"RESPONSE: ===============================")
        logger.debug(f"RESPONSE: {response}")

    # Remove file once finished
    os.remove(datafile_path)


def parse_data_file(data):
    return data.apply(lambda x: parse_row(x["First"]), axis=1)


def map_message_type_to_message_type_id(func):
    symbols = ["s", "A", "d", "E", "X", "P", "r", "B", "H", "I", "J"]
    ids = list(range(0, 11))
    lut = dict(zip(symbols, ids))

    def wrapped_func(input):
        return lut[input]

    return wrapped_func


# @map_message_type_to_message_type_id
def parse_row(row):
    symbols = ["s", "A", "d", "E", "X", "P", "r", "B", "H", "I", "J"]
    ids = list(range(0, 11))
    lut = dict(zip(symbols, ids))
    return {"timestamp": row[1:9], "message_type_id": lut[row[9:10]]}

