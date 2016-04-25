#!/bin/bash
python -m SimpleHTTPServer &

MANIFEST="page_load_test/test.manifest"
PERF_FILE="output/perf-$(date +"%s").json"

python runner.py $MANIFEST $PERF_FILE 
python submit_to_perfherder.py $PERF_FILE servo/revision.json

# Kill the http server
trap 'kill $(jobs -pr)' SIGINT SIGTERM EXIT
