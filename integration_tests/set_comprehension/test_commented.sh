#!/bin/bash

set -e
set -o pipefail
LOG=`mktemp`
DIRECTORY=$(basename $(dirname $0))

python linter test_data/$DIRECTORY/commented.py | tee $LOG && exit 1
grep -F 'commented.py:5:13: set(' $LOG
grep -F 'commented.py:9:13: set(' $LOG
grep -F 'commented.py:13:10: set(' $LOG
