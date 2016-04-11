#!/bin/bash
python -m SimpleHTTPServer &

python runner.py

# Kill the http server
trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT
