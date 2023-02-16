FROM python:3.10.6

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    libpq-dev \
    gcc \
    tzdata \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#set working directory
WORKDIR /usr/src/app

#set environment variables
ENV DOCKER_CONTAINER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8

#install dependencies
RUN pip install --upgrade pip
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev

#copy the api_service project
COPY ./pix_api .
