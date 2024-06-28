
.PHONY: default lint test docs serve=docs run venv

default: lint

lint:
	hatch run lint:all

test:
	hatch run test

docs:
	hatch run docs

serve-docs:
	hatch run serve-docs

shell:
	hatch shell

run:
	hatch run app

venv:
	python -m venv venv
	./venv/bin/pip install -e .