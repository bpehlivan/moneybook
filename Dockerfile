FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/fittrack
WORKDIR /usr/src/fittrack
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt
RUN  apt-get update && apt-get install -y postgresql-client
ADD . /usr/src/fittrack/
RUN chmod +x entrypoint.sh
