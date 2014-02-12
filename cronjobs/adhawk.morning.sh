#!/bin/bash
TMP_LOG=/home/blannon/tmp_log

logger -t "adhawk.morning" "============ STARTING adhawk.morning.sh  $(date --rfc-3339=seconds) ===================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py import_ad_media 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "import_ad_media" $(cat $TMP_LOG)
fi

unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py get_thumbs 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "get_thumbs" $(cat $TMP_LOG)
fi

unbuffer /home/blannon/make_strips.sh 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "make_strips" $(cat $TMP_LOG)
fi

$MY_PYTHON $DJANGO_PROJECT/manage.py report_ad_media 2> $TMP_LOG
if [ "$?" -eq 1 ]; then
    logger -t "report_ad_media" $(cat $TMP_LOG)
fi

logger -t "adhawk.morning" "---- end adhawk.morning.sh $(date --rfc-3339=seconds) -----"
