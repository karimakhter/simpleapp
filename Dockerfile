FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python python-pip && pip install flask

COPY app.py /opt/

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0
