FROM tensorflow/magenta:latest
MAINTAINER Siavash Khallaghi

RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN apt-get update && apt-get install -y libasound-dev

ADD requirements.txt ./

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY audio    /usr/src/audio
COPY core     /usr/src/app
COPY docs     /usr/src/config
COPY scripts  /usr/src/public
COPY services /usr/src/services
COPY tests    /usr/src/test

ENTRYPOINT /bin/bash
