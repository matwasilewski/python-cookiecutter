.PHONY: help install-precommit-hooks check-bootstrap-dependencies check-uv check-tools check-docker bootstrap setup install update format poetry-check lint-check format-check type-check lint unit unit-coverage gcp-authenticate

PYTHON_VERSION?=$(shell cat .python-version | tr -d '[:space:]')
VENV?=.venv
VENV_ACTIVATE=$(VENV)/bin/activate
PYTHON=$(VENV)/bin/python
PIP = $(VENV)/bin/pip

RED="\033[0;31m"
CYAN="\033[36m"
NC="\033[0m"

## help: Prints the names and descriptions of all targets
help:
	@grep -E '## .*$$' $(MAKEFILE_LIST) | grep -v '@grep' | awk 'BEGIN {FS = ": "}; {sub(/^## /, "", $$1); printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# check-bootstrap-dependencies: Check if bootstrap dependencies are installed
check-bootstrap-dependencies:
	@which uv >/dev/null || (echo $(RED)"Error: uv not found. Install from https://github.com/astral-sh/uv and then do: make bootstrap"$(NC); exit 1)
	@echo "uv is installed!"

check-tools:
	@which gcloud > /dev/null || (echo $(RED)"Error: gcloud is not installed. Please install it from https://cloud.google.com/sdk/docs/quickstarts"$(NC); exit 1)
	@echo "gcloud is installed!"
	@which gsutil > /dev/null || (echo $(RED)"Error: gsutil is not installed. Please install it from https://cloud.google.com/storage/docs/gsutil_install"$(NC); exit 1)
	@echo "gsutil is installed!"
	@which docker > /dev/null || (echo $(RED)"Error: docker is not installed. Please install this and ensure its running"$(NC); exit 1)
	@echo "docker is installed!"
	@echo "All prerequisites are installed."

check-docker:
	@echo "Checking if Docker CLI is available..."
	@which docker > /dev/null || (echo "Docker CLI not found. Please install Docker https://www.docker.com/get-started/"$(NC); exit 1;)
	@echo "Docker CLI is available."
	@echo "Checking if Docker is running..."
	@docker ps > /dev/null 2>&1 || (echo $(RED)"Error: Docker is not running. Please start the Docker daemon."$(NC); exit 1;)
	@echo "Docker is running."

bootstrap:
	uv python install --python-preference='only-managed' $(PYTHON_VERSION)	
	@echo "Python $(PYTHON_VERSION) is installed!"

$(VENV_ACTIVATE):
	uv venv --python-preference='only-managed'
	$(PYTHON) -m ensurepip --upgrade
	$(PYTHON) -m pip install --upgrade pip
	@echo "pip is installed!"
	
install-precommit-hooks: $(VENV_ACTIVATE)
	$(PIP) install pre-commit
	$(VENV)/bin/pre-commit install --install-hooks
	@echo "pre-commit is installed!"

precommit: precommit-hooks
	git fetch origin
	$(VENV)/bin/pre-commit run -s origin/main -o HEAD
	
install: $(VENV_ACTIVATE)
	@echo "Installing dependencies..."
	uv pip compile pyproject.toml -o requirements.txt	
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed!"

# TODO: Fix this
update: $(VENV_ACTIVATE)
	uv lock
	uv install --no-root
	@echo "Dependencies updated!"
	@echo "Dont forget to commit the updated lock file"

format: $(VENV_ACTIVATE)
	$(VENV)/bin/ruff check --fix --exit-zero .
	$(VENV)/bin/ruff format .
	@echo "Code formatted!"

# TODO: Fix this
lint-check: $(VENV_ACTIVATE)
	$(POETRY) run ruff check .

# TODO: Fix this
format-check: $(VENV_ACTIVATE)
	$(POETRY) run ruff format --check .

# TODO: Fix this
type-check:
	$(POETRY) run mypy .

## lint: Run all lint checks
# TODO: Fix this
lint: poetry-check lint-check format-check type-check

## unit: Run unit tests
# TODO: Fix this
unit: $(VENV_ACTIVATE)
	$(POETRY) run pytest tests/unit

## unit-coverage: Run unit tests with coverage report
# TODO: Fix this
unit-coverage: $(VENV_ACTIVATE)
	$(POETRY) run coverage run -m pytest tests/unit
	$(POETRY) run coverage report
	$(POETRY) run coverage html

## gcp-authenticate: Authenticate with GCP, use this before running composer commands
gcp-authenticate:
	gcloud auth application-default login
	gcloud auth login

