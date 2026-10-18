SHELL := bash
.DEFAULT_GOAL := help

.PHONY: install
install: ## Create the virtual environment with all dependency groups
	@uv sync

.PHONY: lint
lint: ## Lock consistency, ruff, and mypy
	@uv lock --locked
	@uv run ruff check .
	@uv run ruff format --check .
	@uv run mypy

.PHONY: test
test: ## Tests with coverage (fails under the threshold in pyproject.toml)
	@uv run pytest --cov --cov-report=term-missing

.PHONY: verify
verify: lint test ## The one gate: run before reporting any change complete

.PHONY: build
build: ## Build sdist and wheel into dist/
	@uv build

.PHONY: docs-test
docs-test: ## Build the docs strictly
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Serve the docs locally
	@uv run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'
