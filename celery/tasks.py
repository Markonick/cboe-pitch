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

from app.services import PitchListService

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("CELERY-TASKS")

# Get env vars
endpoint = os.environ.get("PITCH_ENDPOINT")
broker = os.environ.get("CELERY_BROKER_URL")
backend = os.environ.get("CELERY_RESULT_BACKEND")
datafile = os.environ.get("DATA_FILE")
basedir = os.path.abspath(os.path.dirname(__file__))
fpath = os.path.join(basedir, datafile)

celery = Celery(broker=broker, backend=backend)
pitch_list_svc = PitchListService()
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
    This task will run every 10 seconds to check if there is a new data file to process and upload
    """
    try:
        # Check if file in data file is in expected input path location
        path = pathlib.Path(fpath)
        if not path.exists():
            logger.debug(f"DATA FILE DOES NOT EXIST!!")
            return

        chunksize = 1000
        names = ["First", "Second"]

        # Post chunks of 1000 rows to API endpoint
        for chunk in pd.read_csv(fpath, chunksize=chunksize, delim_whitespace=True, header=None, names=names):
            # Parse data file
            parsed_pitch_data_df = parse_data_file(chunk)
            data = parsed_pitch_data_df.tolist()

            response = post_data(data)  # Call post
    except Exception as exc:
        logger.debug(f"UPLOAD PITCH DATA EXCEPTION: {exc}")
    finally:
        # Clean up, remove data file
        path = pathlib.Path(fpath)
        if path.exists():
            os.remove(fpath)


def post_data(body):
    """
    POST data to pitch api endpoint
    """
    try:
        headers = {"Content-Type": "application/json"}
        data_json = json.dumps(body)
        return requests.post(endpoint, data=data_json, headers=headers)
    except OperationalError as exc:
        raise self.retry(exc=exc)  # exponential backoff


def parse_data_file(data):
    return data.apply(lambda x: parse_row(x["First"]), axis=1)


def parse_row(row):
    symbols = ["s", "A", "d", "E", "X", "P", "r", "B", "H", "I", "J"]
    ids = list(range(0, 11))
    lut = dict(zip(symbols, ids))
    return {"timestamp": row[1:9], "message_type_id": lut[row[9:10]]}
