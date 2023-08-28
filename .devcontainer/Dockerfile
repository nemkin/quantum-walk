FROM python:3.10

RUN apt update
    apt install -y sudo

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt
