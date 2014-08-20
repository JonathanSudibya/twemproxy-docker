#!/bin/bash

main() {
  /usr/bin/python3 /generate_configs.py
  /usr/bin/supervisord
}

main
