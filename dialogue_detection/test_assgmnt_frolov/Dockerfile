FROM ubuntu

RUN apt-get update
RUN apt-get -y install python3.6 unzip

COPY start.sh .

ENTRYPOINT ./start.sh && /bin/bash
