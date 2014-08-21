FROM ubuntu:14.04


RUN apt-get update
RUN apt-get install python-pip -qy

RUN pip install python-memcached

ADD test.py /test.py


CMD ["/usr/bin/python", "/test.py"]
