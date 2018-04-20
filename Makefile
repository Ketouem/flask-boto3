excludes = \*~ \*.pyc .cache/\* test_\* __pycache__/\*

TEST_RESULTS_FOLDER ?= .

.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete

.PHONY: test
test:
	nosetests --with-xunit --xunit-file=${TEST_RESULTS_FOLDER}/nosetests.xml --cover-branches --with-coverage --cover-erase --cover-package=flask_boto3 --cover-html --cover-html-dir=${TEST_RESULTS_FOLDER}/cover

.PHONY: bandit
bandit:
	bandit -r flask_boto3/

.PHONY: coveralls
coveralls:
	coveralls
