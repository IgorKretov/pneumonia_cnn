# build on top of the given image
FROM python:3.7-slim
MAINTAINER Samuel Kim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add a dependency for opencv
RUN apt-get update
RUN apt-get install -y libglib2.0-0

RUN mkdir /project
WORKDIR /project
COPY ./project /project

RUN useradd -u 1122 user
USER user
