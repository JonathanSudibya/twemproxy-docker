FROM phusion/baseimage

RUN apt-get update
RUN apt-get install libtool make automake supervisor curl python2.7 python-pip -qy libyaml-0-2 -yq

# Install twemproxy
RUN curl -qL https://github.com/twitter/twemproxy/archive/v0.4.0.tar.gz | tar xzf -
RUN cd v0.4.0 && ./configure --enable-debug=log && make && make install

# install pip deps
RUN pip install pyaml==14.05.7 

# Configuration
RUN mkdir -p /etc/nutcracker
RUN mkdir -p /var/log/nutcracker
ADD generate_configs.py /generate_configs.py
ADD run.sh /run.sh
RUN chmod a+x run.sh

EXPOSE 22121
CMD ["/run.sh"]
