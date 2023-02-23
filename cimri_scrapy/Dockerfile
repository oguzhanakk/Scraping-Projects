FROM amazon/aws-lambda-python:3.9

ENV PYTHONUNBUFFERED True

# install yum
RUN yum -y install tar
RUN yum -y install gzip

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt
#RUN pip install --target "./package" --no-cache-dir -r requirements.txt

# CMD exec gunicorn --bind :8080 --timeout 0 main:app