#!/usr/bin/env bash

echo -e "[distutils]
index-servers=pypi
[pypi]
username = $PYPI_USER
password = $PYPI_PASSWORD
" > ~/.pypirc

pipenv lock --requirements > requirements.txt
python setup.py sdist
twine upload dist/Flask-Boto3-$CIRCLE_TAG.tar.gz
