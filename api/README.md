Water Stress Index API
======================

Introduction
------------

Upstream API for an app that shows Global Water Stress Index.

Development
-----------

You'll need Python 3.6+ and [Poetry](https://poetry.eustace.io/) for dependency management.

```bash
# Install poetry
pip install poetry

# Now install dependencies
poetry install

# Add a dependency
poetry add some_library

# Start the development server and go to http://127.0.0.1:5000/
env FLASK_APP=wsi_api FLASK_DEBUG=1 poetry run flask run

# I personally like the Gunicorn server...
gunicorn wsi_api:app --reload
```

Deployment
----------

See the notes in the `README` above this folder.

Authors
-------

Team 102, CSE6242, Fall 2019, @GATech

License
-------

MIT
