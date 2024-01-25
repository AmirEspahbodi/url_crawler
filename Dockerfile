FROM python:3.12.1-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /url_crawler
WORKDIR /url_crawler

RUN apt-get update && \
    apt-get -y install pkg-config build-essential python3-dev default-libmysqlclient-dev libpq-dev


COPY ./requirements.txt .
RUN pip install --upgrade setuptools && \
    pip install -r requirements.txt --no-cache-dir

COPY ./server /url_crawler
