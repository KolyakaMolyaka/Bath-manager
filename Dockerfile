FROM python:3.11-slim-buster
WORKDIR /usr/src/app

RUN apt-get update
RUN pip install --upgrade pip

COPY . .
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]