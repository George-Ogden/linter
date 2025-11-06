#!/bin/bash

set -e
set -o pipefail
LOG=`mktemp`
DIRECTORY=$(basename $(dirname $0))

python main.py test_data/$DIRECTORY/commented.py | tee $LOG && exit 1
grep -F 'False' $LOG | wc -l | grep -q 5
! grep -F 'True' $LOG
