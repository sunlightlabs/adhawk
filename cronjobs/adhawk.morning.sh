#!/bin/bash

(
echo "============ STARTING adhawk.morning.sh  $(date --rfc-3339=seconds) ===================="
MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py import_ad_media
unbuffer $MY_PYTHON $DJANGO_PROJECT/manage.py get_thumbs
unbuffer /home/blannon/make_strips.sh

$MY_PYTHON $DJANGO_PROJECT/manage.py report_ad_media

echo "---- end adhawk.morning.sh $(date --rfc-3339=seconds) -----"
)
