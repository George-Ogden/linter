#!/bin/bash

set -e
set -o pipefail
DIRECTORY=$(basename "$(dirname $0)")
LOG=`mktemp`

python linter --fix test_data/$DIRECTORY/{,no_}errors.py --fix | tee $LOG && exit 1
grep -F "5 fixes applied" $LOG
diff test_data/$DIRECTORY/{errors.py,expected.py}
git diff --quiet test_data/$DIRECTORY/no_errors.py
