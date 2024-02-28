#!/bin/bash
pip install -r requirements.txt
echo "Requirements are installed"
echo "Starting app..."
flask run -h 0.0.0.0
echo "App started!"