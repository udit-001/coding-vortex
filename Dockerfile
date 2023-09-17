FROM python:3.7-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY ./src/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./src /app
