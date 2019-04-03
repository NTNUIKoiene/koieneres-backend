#!/bin/bash

/snap/bin/docker-compose -f /root/koieneres-backend/docker-compose.yml run certbot renew --dry-run \
&& /snap/bin/docker-compose -f /root/koieneres-backend/docker-compose.yml kill -s SIGHUP webserver