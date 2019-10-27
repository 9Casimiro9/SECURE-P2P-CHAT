FROM python:3.7-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

#RUN apk add --no-cache bash

COPY src .