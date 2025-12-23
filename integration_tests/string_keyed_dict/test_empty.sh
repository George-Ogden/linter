#!/bin/bash

set -e
DIRECTORY=$(basename "$(dirname $0)")

python linter test_data/$DIRECTORY/empty.py
