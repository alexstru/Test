#!/bin/bash
_filename=$(date +"%m_%d_%Y")

python manage.py print_objects_count > ${_filename}.dat