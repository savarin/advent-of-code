#!/bin/bash

# Stop on the first error
set -e

# Run ruff for code formatting check
echo "Running ruff..."
ruff format --check .

# Run pyflakes for static code analysis
echo "Running pyflakes..."
pyflakes .

# Run mypy for type checking
echo "Running mypy..."
mypy . --strict --exclude 2022/src/

# Run pytest for running unit tests
echo "Running pytest..."
pytest

echo "All checks passed!"
