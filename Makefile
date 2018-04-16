excludes = \*~ \*.pyc .cache/\* test_\* __pycache__/\*

.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete

.PHONY: test
test:
	nosetests --with-xunit --cover-branches --with-coverage --cover-erase --cover-package=flask_boto3 --cover-html

.PHONY: bandit
bandit:
	bandit -r flask_boto3/

.PHONY: coveralls
coveralls:
	coveralls
