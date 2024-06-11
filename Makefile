
.PHONY: default lint

default: lint

lint:
	hatch run lint:all

test:
	hatch run test

docs:
	hatch run docs

shell:
	hatch shell
