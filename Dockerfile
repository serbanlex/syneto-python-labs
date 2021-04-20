FROM python:3.9.2-alpine3.12

RUN apk add curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN mkdir -p /home/syneto_labs

WORKDIR /home/syneto_labs

COPY ./pyproject.toml ./pyproject.toml

RUN /root/.poetry/bin/poetry install

EXPOSE 8000