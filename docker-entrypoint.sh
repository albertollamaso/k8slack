#!/bin/bash
set -e
/etc/init.d/nginx start
/usr/bin/python3.7 api.py