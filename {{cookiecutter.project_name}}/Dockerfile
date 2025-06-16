FROM python:3.11-slim AS base

# Install the `uv` package manager (static binary)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establish application directory
WORKDIR /app

# Copy dependency definitions first (for better Docker layer caching)
COPY ./pyproject.toml ./uv.lock* /app/

# Allow an alternative package repository to be provided at build time
ARG PACKAGE_REPO_URL

# Install project dependencies (production only)
#   --no-editable : install the project as a wheel, not editable
#   --no-dev      : skip dev / test dependencies to keep image slim
RUN if [ -n "$PACKAGE_REPO_URL" ]; then \
    uv sync --no-editable --no-dev --extra-index-url "$PACKAGE_REPO_URL"; \
    else \
    uv sync --no-editable --no-dev; \
    fi

# Ensure the environment executables are discoverable
ENV PATH="/app/.venv/bin:$PATH"

# Copy the remainder of the source code
COPY . /app

# Drop privileges for runtime security
RUN useradd -ms /bin/bash service
USER service

# --- Runtime -----------------------------------------------------------------
# Replace the placeholder below with your actual entrypoint, e.g.:
# CMD ["uv", "run", "python", "-m", "my_project.cli"]
CMD ["uv", "run", "python", "-m", "your_package"]
# FIXME: change the module above to your actual application entrypoint


