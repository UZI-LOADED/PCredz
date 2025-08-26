#!/bin/bash
# Start PCredz Dashboard with Gunicorn for production use
# Usage: ./start_dashboard.sh

GUNICORN=$(which gunicorn)
if [ -z "$GUNICORN" ]; then
  echo "Gunicorn is not installed. Installing..."
  pip3 install gunicorn
fi

echo "Starting PCredz Dashboard on http://0.0.0.0:5000 ..."
gunicorn -w 2 -b 0.0.0.0:5000 dashboard:app
