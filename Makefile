
.PHONY: default lint

default: lint

lint:
	hatch run lint:all