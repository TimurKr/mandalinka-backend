#syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/mandalinka/web 

COPY requirements.txt /usr/src/mandalinka/web
RUN pip install -r requirements.txt

COPY . /usr/src/mandalinka/web
