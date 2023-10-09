FROM python:3.11

WORKDIR /srv/project/

COPY ./requirements.txt /srv/project/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /srv/project/app
COPY ./logs /srv/project/logs
COPY ./alembic.ini /srv/project/alembic.ini
COPY ./migrations /srv/project/migrations
COPY ./run.sh /srv/project/run.sh

CMD ["sh", "run.sh"]
