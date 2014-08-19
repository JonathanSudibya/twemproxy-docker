FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install ruby1.9.1 ruby1.9.1-dev libtool make automake supervisor curl -qy

RUN apt-get install -y memcached

# Install twemproxy
RUN curl -qL https://twemproxy.googlecode.com/files/nutcracker-0.3.0.tar.gz | tar xzf -
RUN cd nutcracker-0.3.0 && ./configure --enable-debug=log && make && mv src/nutcracker /twemproxy
RUN cd / && rm -rf nutcracker-0.3.0

# install nutcracker web
RUN gem install nutcracker-web 

# Configuration
RUN mkdir -p /etc/nutcracker
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD config.yaml /etc/nutcracker/memcache.yaml


EXPOSE 3000 22222 22123
CMD ["/usr/bin/supervisord"]
