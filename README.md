Predicting & Visualizing Water Stress Index (WSI)
=================================================

A project by the one and only Team 102 🎸💃🙌 for CSE 6242 @GATech.

Development
-----------

* Web interface in `./ui`
* Python/Flask API in `./api`

See `README.md` in each for further instructions. Here's a TL;DR

```bash
# In one session (in a Virtual Environment)
gunicorn api.wsi_api:app --reload

# In another session,
yarn && yarn start
```

Then go to `http://localhost:3000/` 🤘

Deployment
----------

TODO: Finish this section

### EC2/ECS Bootstrap

```bash
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
```

Members
-------

* J Michael Tritchler
* Heylim Yang
* Spencer Price
* Yatish Kasaraneni
* Deepti Anand
* Nikhil Anand

