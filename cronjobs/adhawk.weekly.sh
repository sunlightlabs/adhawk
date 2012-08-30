#!/bin/bash

(
echo "=============== starting adhawk.weekly.sh $(date --rfc-3339=seconds) ================"
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py import_fec
$MY_PYTHON $DJANGO_PROJECT/manage.py update_fec_kb
$MY_PYTHON $DJANGO_PROJECT/manage.py initalize_funder_families

echo "------------- ending adhawk.weekly.sh $(date --rfc-3339=seconds) ------------------"
)
