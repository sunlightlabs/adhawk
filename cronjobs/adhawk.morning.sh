#!/bin/bash
TMP_LOG=/home/blannon/tmp_log

logger -t "adhawk.morning" "============ STARTING adhawk.morning.sh  $(date --rfc-3339=seconds) ===================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py import_ad_media 2>&1 | logger -t "import_ad_media"

$MY_PYTHON $DJANGO_PROJECT/manage.py get_thumbs 2>&1 | logger -t "get_thumbs"

/home/blannon/make_strips.sh 2>&1 | logger -t "make_strips"

$MY_PYTHON $DJANGO_PROJECT/manage.py report_ad_media 2>&1 | logger -t "report_ad_media"

logger -t "adhawk.morning" "======== end adhawk.morning.sh $(date --rfc-3339=seconds) ======"
