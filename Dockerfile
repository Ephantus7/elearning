# pull official base image

FROM python:3.12.0b4-slim-bullseye

# set work directory

WORKDIR /usr/src/elearning

# set environment variables

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

RUN pip install --upgrade pip

COPY ./requirements.txt .

# install dependencies for postgres

RUN apt-get update && apt-get install -y libpq-dev gcc

# install dependencies for pillow

RUN apt-get install -y libjpeg-dev zlib1g-dev

# install dependencies for cffi

RUN apt-get install -y libffi-dev


RUN pip install -r requirements.txt

# copy project

COPY . .
