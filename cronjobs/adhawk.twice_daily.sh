#!/bin/bash

(
echo "================== starting adhawk.twice_daily.sh $(date --rfc-3339=seconds) ===============" 
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py import_ftum
unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py rank_top_ads

echo "------------ end adhawk.twice_daily.sh $(date --rfc-3339=seconds) -----------"
)
