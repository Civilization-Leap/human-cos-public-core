# Human-COS Runtime — S0 development / test image.
# S0 scope: pure-Python package + tests. No DB or services required yet.
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy package metadata first for better layer caching.
COPY pyproject.toml README.md ./
COPY src ./src

# Install package (+ dev extras for running tests inside the image).
RUN pip install --upgrade pip \
    && pip install -e ".[dev]"

# Test suite and data contracts.
COPY tests ./tests
COPY schemas ./schemas
COPY protocols ./protocols
COPY migrations ./migrations

# S0 default command: run the full test suite from a clean image.
CMD ["pytest", "-q"]
