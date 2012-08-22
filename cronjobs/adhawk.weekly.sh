#!/bin/bash

MY_PYTHON=/home/blannon/.virtualenvs/whopaid/bin/python
DJANGO_PROJECT=/home/blannon/whopaid

$MY_PYTHON $DJANGO_PROJECT/manage.py import_fec
$MY_PYTHON $DJANGO_PROJECT/manage.py update_fec_kb
$MY_PYTHON $DJANGO_PROJECT/manage.py initalize_funder_families

