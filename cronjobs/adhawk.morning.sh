#!/bin/bash

MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py import_ad_media
$MY_PYTHON $DJANGO_PROJECT/manage.py get_thumbs
/home/blannon/make_strips.sh

$MY_PYTHON $DJANGO_PROJECT/manage.py report_ad_media

