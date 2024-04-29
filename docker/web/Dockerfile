# SERVER
FROM --platform=linux/amd64 python:3.11.8-alpine as build

WORKDIR /home/app
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apk add --no-cache ffmpeg

COPY .env .env