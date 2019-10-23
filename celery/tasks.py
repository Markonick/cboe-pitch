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

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
logger = logging.getLogger("CELERY-TASKS")

# Get env vars
endpoint = os.environ.get("PITCH_ENDPOINT")
broker = os.environ.get("CELERY_BROKER_URL")
backend = os.environ.get("CELERY_RESULT_BACKEND")

celery = Celery(broker=broker, backend=backend)

# Add periodic tasks to scheduler
@celery.on_after_configure.connect
def add_periodic_task(sender, **kwargs):
    sender.add_periodic_task(5.0, upload_pitch_data("input/"), name="Create new pitch data every 30 sec, if available")


@celery.task
def upload_pitch_data(file_path):
    logger.info(f"UPLOAD NEW PITCH DATA - Before call!!!! ENDPOINT: {endpoint}")

    # Check if file in data file is in expected input path location
    for pitch_data_file in glob.glob(file_path):
        raw_pitch_data = pd.read_csv(pitch_data_file, sep=" ", header=None)
        parsed_pitch_data = parse_data_file(raw_pitch_data)
        os.remove(pitch_data_file)

        headers = {"Content-Type": "application/json"}
        data_json = json.dumps(parsed_pitch_data)
        logger.debug(f"DATA: {parsed_pitch_data}")
        response = requests.post(endpoint, data=data_json, headers=headers)


def parse_data_file(data):
    # return [parse_row(row) for row in data.iterrrows()]
    return data.apply(lambda x: parse_row(x))


def parse_row(row):
    parsed_row = {"timestamp": row[0:9], "message_type": row[8:9]}

    return parsed_row
