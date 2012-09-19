#!/bin/bash

(
echo "============ starting adhawk.evening.sh  $(date --rfc-3339=seconds) =================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py download_videos
$MY_PYTHON $DJANGO_PROJECT/manage.py ingest_fingerprints
$MY_PYTHON $DJANGO_PROJECT/manage.py update_index

echo "------- end adhawk.evening.sh  $(date --rfc-3339=seconds) -------------------"
)
