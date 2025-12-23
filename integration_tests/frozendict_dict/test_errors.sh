#!/bin/bash

set -e
set -o pipefail
DIRECTORY=$(basename "$(dirname $0)")
LOG=`mktemp`

python linter test_data/$DIRECTORY/indirect.py | tee $LOG && exit 1
grep -F 'indirect.py:3:7: frozendict.frozendict(dict(keys="values"))' $LOG
grep -F 'indirect.py:5:10: frozendict.frozendict(**bad)' $LOG
