#!/bin/sh
gunicorn --workers=10 --threads=8 --timeout=5400 --access-logfile - -b 0.0.0.0:5555 app:app