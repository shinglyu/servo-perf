#!/bin/bash
python -m SimpleHTTPServer &

python runner.py $1

# Kill the http server
trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT
