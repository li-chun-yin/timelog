#!/bin/bash

mongod &
uwsgi --ini /app/uwsgi.ini &
nginx -g "daemon off;"