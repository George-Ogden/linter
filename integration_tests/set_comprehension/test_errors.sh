#!/bin/bash

set -e
set -o pipefail
DIRECTORY=$(basename $(dirname $0))
LOG=`mktemp`

python main.py test_data/$DIRECTORY/errors.py | tee $LOG && exit 1
grep -F 'errors.py:1:8: set(x for x in range(5))' $LOG
grep -F 'errors.py:3:13: set((y for y in range(6)))' $LOG
grep -F 'errors.py:5:13: set(' $LOG
grep -F 'errors.py:9:24: set({z for z in range(len(set(u for u in range(6))))})' $LOG
grep -F 'errors.py:9:50: set(u for u in range(6))' $LOG
