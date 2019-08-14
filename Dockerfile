FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/moneybook
WORKDIR /usr/src/moneybook
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt
RUN  apt-get update && apt-get install -y postgresql-client
ADD . /usr/src/moneybook/
RUN chmod +x entrypoint.sh
