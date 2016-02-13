#!/usr/bin/env bash

find . -name '*.pyc' -delete
find . -name "*.egg-info" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*__pycache__" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*.eggs" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*.cache" -type d -exec rm -r "{}" \;  2> /dev/null

python setup.py test

find . -name '*.pyc' -delete
find . -name "*.egg-info" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*__pycache__" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*.eggs" -type d -exec rm -r "{}" \;  2> /dev/null
find . -name "*.cache" -type d -exec rm -r "{}" \;  2> /dev/null
