.PHONY: help check-bootstrap-dependencies check-tools check-docker bootstrap precommit install format type-check unit gcp-authenticate

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

## check-tools: Check if required tools are installed
check-tools:
	@which gcloud > /dev/null || (echo $(RED)"Error: gcloud is not installed. Please install it from https://cloud.google.com/sdk/docs/quickstarts"$(NC); exit 1)
	@echo "gcloud is installed!"
	@which gsutil > /dev/null || (echo $(RED)"Error: gsutil is not installed. Please install it from https://cloud.google.com/storage/docs/gsutil_install"$(NC); exit 1)
	@echo "gsutil is installed!"
	@which docker > /dev/null || (echo $(RED)"Error: docker is not installed. Please install this and ensure its running"$(NC); exit 1)
	@echo "docker is installed!"
	@echo "All prerequisites are installed."

## check-docker: Check if Docker CLI is available
check-docker:
	@echo "Checking if Docker CLI is available..."
	@which docker > /dev/null || (echo "Docker CLI not found. Please install Docker https://www.docker.com/get-started/"$(NC); exit 1;)
	@echo "Docker CLI is available."

## bootstrap: Install Python version and pipx
bootstrap: check-bootstrap-dependencies check-tools check-docker
	uv python install --python-preference='only-managed' $(PYTHON_VERSION)
	@echo "Python $(PYTHON_VERSION) is installed!"

## $(VENV_ACTIVATE): Create a virtual environment
$(VENV_ACTIVATE): check-bootstrap-dependencies
	uv venv --python-preference='only-managed'
	$(PYTHON) -m ensurepip --upgrade
	$(PYTHON) -m pip install --upgrade pip
	@echo "pip is installed!"

## .git/hooks/pre-commit: Install pre-commit hooks
.git/hooks/pre-commit: $(VENV_ACTIVATE)
	$(PIP) install pre-commit
	$(VENV)/bin/pre-commit install --install-hooks
	@echo "pre-commit is installed!"

## precommit: Run pre-commit hooks
precommit: .git/hooks/pre-commit
	git fetch origin
	$(VENV)/bin/pre-commit run -s origin/main -o HEAD

## install: Install dependencies
install: $(VENV_ACTIVATE)
	@echo "Installing dependencies..."
	uv pip compile pyproject.toml -o requirements.txt
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed!"

## format: Format code
format: $(VENV_ACTIVATE)
	$(VENV)/bin/ruff check --fix --exit-zero .
	$(VENV)/bin/ruff check --select I --fix
	$(VENV)/bin/ruff format .
	@echo "Code formatted!"

## type-check: Type check code with mypy
type-check:
	$(VENV)/bin/mypy .

## unit: Run unit tests
unit: $(VENV_ACTIVATE)
	$(VENV)/bin/pytest tests/unit

## gcp-authenticate: Authenticate with GCP, use this before running composer commands
gcp-authenticate:
	gcloud auth application-default login
	gcloud auth login
