install:
	poetry install

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

check:
	make lint
	make test

build:
	make check
	poetry build