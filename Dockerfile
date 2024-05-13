# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
COPY /static $APP_HOME/static

EXPOSE 8000
COPY . .
