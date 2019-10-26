# CBOE PITCH DATA API
A simple class-based Flask API (flask-restplus) with a Celery beat scheduler, dockerised.


PREREQUISITES
-------------
i) Docker

ii) docker-compose

iii) pipenv

This solution can run in pipenv mode without celery/redis.


ENVIRONMENT
-----------

Create a .env file in the root directory and add the following:

    FLASK_APP=run.py
    PITCH_ENDPOINT=http://backend:5000/api/v1/pitch
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    DATABASE_URL=postgresql://postgres:admin@cboe-db:5432/pitch
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=admin
    DATA_FILE=pitch_data.txt
    PER_PAGE=50

PIP
---

All you need to do is a

    pipenv shell

and then

    pip install -r requirements.txt
  
this should create an cboe virtual environment to work within

TESTING
-------

To run the functional tests do

    pytest -v

FULL APP WITH CELERY BEAT
-------------------------

In order to run the celery tasks, we need to run 5 docker containers.

i) Flask backend

ii) Celery beat scheduler

iii) Celery worker

iv) Redis queue

v) Flower (Web based GUI task monitor)

To start the app, do a

    docker-compose up --build
    
This should kick-off all containers. You can observe the supported API endpoints in Swagger at

    http://localhost:5000/
    
![alt text](images/swagger1.png)

Eg. clciking on the GET methdo, we can execute a get list command:

![alt text](images/swagger2-post.png)
and the Flower monitor at 

    http://127.0.0.1:5555/tasks
    
![alt text](images/flower.png)

Instructions
------------

![alt text](images/cboe-website.png)
![alt text](images/term-no-tasks.png)


sudo rm celery/pitch_data.txt
cp pitch_data.txt celery

![alt text](images/term-with-tasks.png)

To run a virtualenv, use pipenv:

    pipenv shell

![alt text](images/pip-shell.png)

Then install requirements:

    pip install -r requirements.txt