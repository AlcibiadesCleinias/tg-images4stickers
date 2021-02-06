FROM ubuntu:16.04
FROM python:3.9.1-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR script/

# preparation for Pillow install
# https://github.com/python-pillow/Pillow/issues/1763
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

COPY ./requirements.txt /script/requirements.txt
RUN pip install -r /script/requirements.txt
COPY . /script/

ENTRYPOINT ["python", "resize_optimize_images4tg.py"]
