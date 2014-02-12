#!/bin/bash
TMP_LOG=/home/blannon/tmp_log

logger -t "adhawk.evening" "============ starting adhawk.evening.sh  $(date --rfc-3339=seconds) =================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py download_videos 2>&1 | logger -t "download_video"

$MY_PYTHON $DJANGO_PROJECT/manage.py ingest_fingerprints 2>&1 | logger -t "ingest_fingerprints"

$MY_PYTHON $DJANGO_PROJECT/manage.py update_index 2>&1 | logger -t "update_index"

logger -t "adhawk.evening" "========= end adhawk.evening.sh  $(date --rfc-3339=seconds) ============"
