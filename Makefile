install:
	poetry install

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8

page-loader:
	poetry run page-loader

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader/ tests/ --cov-report xml

check: selfcheck lint test

build:
	rm -rf dist
	poetry build

deploy:
	make build
	make package-install
	page-loader --output /Users/ruslan/Desktop/python-project-lvl3/tmp https://www.gov.uk/

.PHONY: install test lint selfcheck check build page_loader deploy test-coverage