#!/bin/bash
TMP_LOG=/home/blannon/tmp_log

logger -t "adhawk.evening" "============ starting adhawk.evening.sh  $(date --rfc-3339=seconds) =================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py download_videos 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "download_video" $(cat $TMP_LOG)
fi

$MY_PYTHON $DJANGO_PROJECT/manage.py ingest_fingerprints 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "ingest_fingerprints" $(cat $TMP_LOG)
fi

$MY_PYTHON $DJANGO_PROJECT/manage.py update_index 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "update_index" $(cat $TMP_LOG)
fi


logger -t "adhawk.evening" "------- end adhawk.evening.sh  $(date --rfc-3339=seconds) -------------------"
