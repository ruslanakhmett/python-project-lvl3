install:
	poetry install

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8

page_loader:
	poetry run page_loader

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

check:
	make lint
	make test

build:
	poetry build

deploy:
	make build
	make package-install
	page_loader --output /hexlet/python-project-lvl3/tmp https://www.gov.uk

.PHONY: install test lint selfcheck check build page_loader deploy test-coverage