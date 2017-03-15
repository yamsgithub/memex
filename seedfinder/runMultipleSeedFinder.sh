#!/bin/bash

SCRIPT_PATH="${BASH_SOURCE[0]}";
SCRIPT_DIR=$(dirname $SCRIPT_PATH)
export ACHE_HOME=$(dirname $(which ache))/../lib/ache/
echo "ACHE_HOME : $ACHE_HOME"
export PATH="$ACHE_HOME/bin:$PATH"
export PYTHONPATH=$DD_API_HOME/../:$DD_API_HOME:$PYTHONPATH
echo "PYTHONPATH: $PYTHONPATH"

python multiple_queries_seedfinder.py


