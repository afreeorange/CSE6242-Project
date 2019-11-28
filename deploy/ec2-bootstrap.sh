#!/bin/bash

yum -y update
yum -y install \
    bzip2-devel \
    git \
    python37

# Would typically install Nginx to proxy to Gunicorn but since we're just
# bundling our static assets (the SPA) into the wheel itself, no need for this.
# Gunicorn listening on port 80/443 will be just fine.

# Now for the usual Python venv drama...
mkdir -p /var/www/wsi
python3 -m venv /var/www/wsi/venv
/var/www/wsi/venv/bin/pip3 install ...
