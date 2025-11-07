#!/bin/bash

set -e
DIRECTORY=$(basename $(dirname $0))

python main.py test_data/$DIRECTORY/empty.py
