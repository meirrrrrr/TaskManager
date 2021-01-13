FROM python:3.8-alpine

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache bash \
    && apk --update add redis
RUN pip install -r requirements.txt
COPY . /code/

COPY ./start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
