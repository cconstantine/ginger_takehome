FROM python:3.9.1-slim-buster as base

RUN apt-get update && apt-get install -y \
 libpq-dev \
 postgresql-client \
 build-essential \
 git \
 curl \
 jq

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ENV HOME="/app"
WORKDIR /app


# Development target
FROM base as dev

#This user schenanigans allows for local development
ARG USER=app
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} ${USER} && \
    useradd -l -u ${USER_ID} -g ${USER} ${USER}

RUN chown ${USER}:${USER} /app
USER ${USER}


# Server target
FROM base as deploy

#This user schenanigans allows running as non-root
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} www && \
    useradd -l -u ${USER_ID} -g www www

RUN chown www:www /app
USER www

COPY --chown=www:www requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY --chown=www:www . /app

EXPOSE 8000
