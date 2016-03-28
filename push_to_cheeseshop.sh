echo -e "[distutils]
index-servers=pypi
[pypi]
repository = https://pypi.python.org/pypi
username = $PYPI_USER
password = $PYPI_PASSWORD
" > ~/.pypirc

python setup.py sdist upload