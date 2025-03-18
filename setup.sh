#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the project dependencies
pip install -r requirements.txt

# Run the Django development server
python manage.py runserver
