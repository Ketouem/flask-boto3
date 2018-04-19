excludes = \*~ \*.pyc .cache/\* test_\* __pycache__/\*


.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete

.PHONY: test
test:
	nosetests --with-xunit --cover-branches --with-coverage --cover-erase --cover-package=flask_boto3 --cover-html

.PHONY: circle_test
circle_test:
	nosetests --with-xunit --xunit-file=test-reports/xunit.xml --cover-branches --with-coverage --cover-erase --cover-package=flask_boto3 --cover-html --cover-html-dir=test-reports/

.PHONY: bandit
bandit:
	bandit -r flask_boto3/

.PHONY: coveralls
coveralls:
	coveralls
