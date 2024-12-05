#!/bin/bash

# # Create virtual environment
# python -m venv venv
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3.12  manage.py collectstatic --noinput
