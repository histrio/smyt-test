.PHONY: docs

init:
	pip install -r REQUIREMENTS

tests:
	nosetests -vv

coverage:
	nosetests -vv --with-coverage --cover-html --cover-package=task -s

build:
	python setup.py clean sdist

