FROM python:2-alpine

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

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
