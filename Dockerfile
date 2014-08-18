FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install ruby1.9.1 ruby1.9.1-dev build-essential supervisor -y

RUN apt-get install -y memcached

RUN gem install nutcracker-web nutcracker

RUN mkdir -p /etc/nutcracker
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ADD config.yaml /etc/nutcracker/memcache.yaml


EXPOSE 3000 22222
CMD ["/usr/bin/supervisord"]
