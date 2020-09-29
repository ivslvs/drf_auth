FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /finance_sys
WORKDIR /finance_sys

ADD requirements.txt /finance_sys/
RUN pip install -r requirements.txt

ADD . /finance_sys/