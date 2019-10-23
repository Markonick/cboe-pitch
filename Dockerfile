FROM python:3.7

EXPOSE 5000

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD python run.py