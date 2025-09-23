#!/bin/bash

# Set PYTHONPATH to include virtual environment packages
export PYTHONPATH="/media/mrx/projects/jobmailer/venv/lib/python3.10/site-packages:$PYTHONPATH"

# Run Django development server
python3 manage.py runserver
