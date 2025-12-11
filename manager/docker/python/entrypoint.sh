#!/usr/bin/env bash
set -euo pipefail

# WORKDIR should be /app (set in Dockerfile)
# Run tests if requested, otherwise jump straight to running the app.
if [ "${RUN_TESTS:-0}" = "1" ] || [ "${RUN_TESTS:-false}" = "true" ]; then
  echo "RUN_TESTS enabled -> running tests before starting the app..."
  # run pytest from /app (WORKDIR). Adjust the path if your tests are located elsewhere.
  pytest -q tests
  PYTEST_EXIT_CODE=$?
  if [ "$PYTEST_EXIT_CODE" -ne 0 ]; then
    echo "Tests failed with exit code $PYTEST_EXIT_CODE. Exiting."
    exit $PYTEST_EXIT_CODE
  fi
  echo "Tests passed. Continuing to start the application."
fi

# Exec the container CMD (e.g., uvicorn) so signals are forwarded correctly
exec "$@"