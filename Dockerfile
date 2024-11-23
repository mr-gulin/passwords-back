FROM python:3.12.2-slim

# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /app

COPY requirements.txt /app/
COPY entrypoint.sh /app/
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc python3-dev default-libmysqlclient-dev build-essential
RUN apt-get install -y apt-utils
RUN apt-get install -y pkg-config
RUN apt-get install -y curl

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
COPY . /app/
