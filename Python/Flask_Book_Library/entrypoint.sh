#!/bin/sh
# Run the unit tests first; start the application only if they all pass.
set -e

echo ">>> Running unit tests..."
# Tests use an in-memory database, so they never touch project/data.sqlite
if ! DATABASE_URL="sqlite:///:memory:" python -m unittest discover -s tests -t . -v; then
    echo ">>> Tests FAILED - application will not be started." >&2
    exit 1
fi

echo ">>> All tests passed - starting the application on port 5000..."
exec flask run
