#!/bin/bash

# Activate virtual environment if needed
# source /path/to/venv/bin/activate

# Start Gunicorn with the gevent worker
# gunicorn app:api -w 4 -k gevent --bind 0.0.0.0:8000
uvicorn app:api --host 0.0.0.0 --port 8000 --reload
