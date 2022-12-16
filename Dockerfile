FROM python:3.10-bullseye as base

RUN useradd -ms /bin/bash galileo

COPY requirements.txt /opt/app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /opt/app/requirements.txt

USER galileo

COPY src/celery_demo /opt/app
COPY uwsgi.ini /opt/app/uwsgi.ini

WORKDIR /opt/app

FROM base as webapp
ENTRYPOINT uwsgi --ini uwsgi.ini

FROM base as worker
ENV WORKER_QUEUE_NAME="celery"
ENV WORKER_LOGLEVEL="INFO"
ENTRYPOINT celery \
    -A celery_demo.celery \
    worker \
    --loglevel=${WORKER_LOGLEVEL} \
    -Q ${WORKER_QUEUE_NAME}