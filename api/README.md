Water Stress Index API
=============================

Introduction
------------

Upstream API for an app that shows Global Water Stress Index

Documentation
-------------

See `docs/`

Development
-----------

```bash
# Set up your virtual environment. This can be via a simple
#
#   python -m venv venv
#   . venv/activate
#
# I prefer pyenv

# Now install dependencies
make dev_install

# Start the server and go to http://127.0.0.1:8000/
gunicorn wsi_api:app

```
Run `make` to see a list of other available options. Note that you _must_ be in a virtual environment to make (heh) most of those tasks work.

Authors
-------

Team 102, CSE6242, Fall 2019, @GATech

License
-------

MIT
