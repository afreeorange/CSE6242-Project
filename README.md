Predicting & Visualizing Water Stress Index (WSI)
=================================================

[![CircleCI](https://circleci.com/gh/afreeorange/CSE6242-Project.svg?style=svg&circle-token=4b95a7d95770cf0d67ae806bb5281aa321ecae69)](https://circleci.com/gh/afreeorange/CSE6242-Project)

An app that visually describes and forecasts Global Water Stress Index. A final project by the one and only Team 102 🎸💃🙌 for CSE 6242 @GATech.

[See it in action here](http://waterstressindex.info/)!

Running
-------

Requires Python 3.6+. In a virtual environment,

```bash
# Just in case
unset DEBUG

# Fetch the latest build artifact. jq would be nicer but 🤷‍♀️
LATEST_WSI_BUILD=$(curl https://api.github.com/repos/afreeorange/CSE6242-Project/releases/latest --silent | python -c "import sys;import json;print(json.loads(''.join(_.strip() for _ in sys.stdin))['assets'][0]['browser_download_url'])")

# Install it
pip install ${LATEST_WSI_BUILD}

# Run it locally at http://127.0.0.1:8000
gunicorn wsi_api:app
```

API Specification
-----------------

### Historical Data and Model Predictions

```
GET /wsi

{
    2015: {
        "Antigua": 32,
        "United_Arab_Emirates": 2048,
        .
        .
    },
    2020: {
        "Antigua": 37,
        "United_Arab_Emirates": 2219,
        .
        .
    },
    .
    .
}
```

### Predictions Based on User Interaction

```
GET /predict?year=2025&gdp_delta=-1&population_delta=2

{
    2025: {
        "Antigua": 56,
        "United_Arab_Emirates": 2487,
        .
        .
    }
}

```

Development
-----------

The API and UI are separate sub-projects which are eventually smushed together at build time to create the deployable artifact.

### API

This is in `./api`. You'll need Python 3.6+ and [Poetry](https://poetry.eustace.io/) for dependency management.

```bash
# Go to the API folder
cd api

# Install poetry. Tip: I manage my Python versions with pyenv and do this
# globally for a given version.
pip install poetry

# Now install app dependencies
poetry install

# You have two options:

# 1) Start the Flask development server. Go to http://127.0.0.1:5000
env FLASK_APP=wsi_api FLASK_DEBUG=1 DEBUG=1 poetry run flask run

# 2) I personally like the Gunicorn server. Go to http://127.0.0.1:8000
env DEBUG=1 poetry run gunicorn wsi_api:app --reload
```

You _will_ see an "Internal Server Error" when you go to the URIs listed above. This is normal. Concern yourself with developing the endpoints in "API Specification".

There are a few tasks in the `Makefile` as well.

```bash
# Clean all build artifacts and Python crud
make clean

# Build the wheel
make build
```

Lastly and importantly: when you're done with your work, and for the deployment to go through successfully, *make sure you update the version in `./api/pyproject.toml`* before you commit and send that MR! Read about [Semantic Versioning](https://semver.org/) before you update. For small patches,

```bash
make bump
# Then the usual git add, commit etc.
```

💫

### Web Interface

As of this writing, it doesn't need a complicated build/watch process. Install something like [`http-server`](https://www.npmjs.com/package/http-server) and do this

```bash
hs ui
```

Deployment
----------

TL;DR: We go from GitHub Repo &rarr; CircleCI &rarr; GitHub Release &rarr; AWS Deployment &rarr; [`http://waterstressindex.info`](http://waterstressindex.info/)

Like with all DevOps, this sounds simple enough until you actually have to do it. Onward.

### GitHub Repo

Any push to `master` will trigger a build. The version in `api/pyproject.toml` is very important: Update it manually or by using `make bump` depending upon the [nature of your changes](https://semver.org/).

### CircleCI

The following has been set up in CircleCI:

* SSH User Key (to execute commands on the EC2 instance)
* GitHub status trigger (set up automagically)
* These environment variables
    - `AWS_DEPLOY_SCRIPT` (keep reading)
    - `AWS_HOST`
    - `AWS_PORT` (please don't use 22. Even better, set up and tear down an SG.)
    - `AWS_USER`
    - `GITHUB_TOKEN`

We're only set up to listen to and deploy upon changes in `master` (i.e., no build branch deployments.) See `./circleci/config.yml` for what happens when you push a change to `master`.

### GitHub Release

One of the steps in the build process is the deposition of a build artifact in GitHub. You can [see them here](https://github.com/afreeorange/CSE6242-Project/releases). Important thing is that the build process is configured to _clobber any existing artifact with the same version number_! Don't do that. At the minimum, `make bump` ♥️

### AWS Deployment

Simplest thing is an EC2 instance. You can run this in ECS as well. Whatever you do, you'll need to (1) set it up and (2) configure a deployment script that CircleCI will run (the `$AWS_DEPLOY_SCRIPT` in an earlier section.)

#### EC2 Bootstrap

You'll need this set up before anything.

Written for the [latest EC2 AMI](https://hub.docker.com/_/amazonlinux/) at the time of this writing: `amazonlinux:2018.03.0.20191014.0-with-sources`

```bash
yum -y update
yum -y install \
    bzip2-devel \
    git \
    python37

# Would typically install Nginx to proxy to Gunicorn but since we're just
# bundling our static assets (the SPA) into the wheel itself, no need for this.
# Gunicorn listening on port 80/443 will be just fine.
#
# Permissions not specified. Assuming you're not going to run this as root.
mkdir -p /var/www/wsi
python3 -m venv /var/www/wsi/venv

# This is the deploy script invoked by CircleCI. Works for a first-time bootstrap.
cat > path_to_script.sh <<EOF
echo "Started `date`" >> /var/www/wsi/deploy.log
export WSI_API_PACKAGE=$(curl https://api.github.com/repos/afreeorange/CSE6242-Project/releases/latest --silent | jq ".assets[0].browser_download_url" | xargs)

echo "Attempting to install ${WSI_API_PACKAGE}" >> /var/www/wsi/deploy.log
/var/www/wsi/venv/bin/pip3 install -U ${WSI_API_PACKAGE}  >> /var/www/wsi/deploy.log 2>&1

echo "Stopping server" >> /var/www/wsi/deploy.log
kill `cat /var/www/wsi/server.pid` >> /var/www/wsi/deploy.log 2>&1

echo "Starting server" >> /var/www/wsi/deploy.log
/var/www/wsi/venv/bin/gunicorn wsi_api:app -b 0.0.0.0:80 -p /var/www/wsi/server.pid -D

echo "---"  >> /var/www/wsi/deploy.log
EOF

chmod +x path_to_script.sh
path_to_script.sh
```

Wherever you choose to keep your script, update CircleCI with it's full path in `$AWS_DEPLOY_SCRIPT`.

Members
-------

* J Michael Tritchler
* Heylim Yang
* Spencer Price
* Yatish Kasaraneni
* Deepti Anand
* Nikhil Anand

License
-------

MIT
