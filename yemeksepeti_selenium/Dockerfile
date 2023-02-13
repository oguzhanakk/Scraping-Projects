FROM python:3.8-slim-buster
# install git
ENV PYTHONUNBUFFERED True
#RUN --memory 4g <command>

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git


COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
#/&& pip install virtualenv 
#virtualenv venv
#source venv/bin/activate
# gunicorn -b 0.0.0.0:8080 --timeout 0 main_crochet:app
# ENTRYPOINT gunicorn --bind :8080 --timeout 0 main_crochet:app
