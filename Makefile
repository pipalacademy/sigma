
.PHONY: default lint

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