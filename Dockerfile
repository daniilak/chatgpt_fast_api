FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv ffmpeg

RUN mkdir -p /code
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /app
EXPOSE 7000

CMD uvicorn main:app --host 0.0.0.0 --port 7000 --root-path /chatgpt