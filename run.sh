#!/bin/bash

main() {
  /usr/bin/python /generate_configs.py
  cat /etc/nutcracker/nutcracker.yml
  /usr/bin/supervisord
}

main
