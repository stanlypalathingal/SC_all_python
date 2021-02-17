#!/bin/bash
FROM arm32v7/python:3.7-slim-buster

RUN apt-get -q update && \
	apt-get -qy install \ 
	libatlas-base-dev \
	libgomp1

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -r requirements.txt 
RUN pip install "pymongo" --no-cache-dir --extra-index-url=https://www.piwheels.org/simple
ADD . /

EXPOSE 9012

ENTRYPOINT ["/bin/bash","./script.sh"]

RUN chmod a+x script.sh

