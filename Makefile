.PHONY: app help test

MSG ?= some msg
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

print-branch:
	@echo "Current branch: $(BRANCH)"

help:
	echo "Available targets:"
	echo "make sure you are in the root directory"
	echo "  help: Show this help message"
	echo "  app: Run the application"
	echo "  test: Run the tests"
	echo "  commit: Commit changes to the repository"
	echo "  push: Push changes to the repository"

app:
	uv run main.py

test:
	uv sync --group test
	uv run python -m pytest app/tests

commit :
	git add .
	git commit -m "$(MSG)"

push:
	git push origin $(BRANCH)

