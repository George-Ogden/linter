#!/bin/bash

set -e
set -o pipefail
DIRECTORY=$(basename $(dirname $0))
LOG=`mktemp`

python linter --fix test_data/$DIRECTORY/{{,no_}errors,combined}.py --fix | tee $LOG && exit 1
grep -F "11 fixes applied" $LOG
diff test_data/$DIRECTORY/{errors.py,expected.py}
diff test_data/$DIRECTORY/combined{,_expected}.py
git diff --quiet test_data/$DIRECTORY/no_errors.py
