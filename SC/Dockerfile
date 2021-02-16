FROM arm32v7/python:3.7-slim-buster

RUN apt-get -q update && \
	apt-get -qy install \ 
	libatlas-base-dev \
	libgomp1

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -r requirements.txt 

ADD . /

EXPOSE 9006
ENTRYPOINT ["/bin/bash","script.sh"]

#ENTRYPOINT ["/bin/bash"]
RUN chmod a+x script.sh

#CMD ["script.sh" ]