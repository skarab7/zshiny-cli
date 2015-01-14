############################################################
# Dockerfile to execute zshiny, a CLI for zalando-shop API
############################################################
FROM ubuntu:14.10
MAINTAINER Wojciech Barczynski (github:skarab7)

ENV ZALANDO_API_ENDPOINT, https://api.zalando.com

RUN apt-get -y update && apt-get install -y python3-pip

ADD requirements.txt /home/
ADD test-requirements.txt /home/
ADD setup.py /home/
CMD mkdir -p /home/shiny_client/
ADD shiny_client/ /home/shiny_client/
CMD mkdir -p /home/test/
ADD test/ /home/test/

WORKDIR /home/
RUN pip3 install -U -r requirements.txt

ENV PYTHONPATH .
ENTRYPOINT ["python3", "shiny_client/shell.py"]
