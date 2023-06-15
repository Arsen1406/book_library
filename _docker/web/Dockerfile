FROM python:3.7-slim

RUN mkdir /app
COPY /requirements.txt /app/
RUN pip install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
COPY . /app
