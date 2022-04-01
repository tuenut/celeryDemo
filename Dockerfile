FROM python:3.10-bullseye

COPY requirements.txt /opt/app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /opt/app/requirements.txt

COPY src/celery_demo /opt/app
COPY uwsgi.ini /opt/app/uwsgi.ini

WORKDIR /opt/app


