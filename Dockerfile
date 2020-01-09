FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    gcc \
    jpeg-dev \
    libmagic \
    libffi-dev \
    linux-headers \
    musl-dev \
    openssl \
    postgresql-dev \
    zlib-dev

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY ./favicon.ico /code/static/favicon.ico

RUN ./manage.py collectstatic --noinput

CMD dockerize -wait tcp://db:5432 && ./manage.py runserver 0.0.0.0:8000
