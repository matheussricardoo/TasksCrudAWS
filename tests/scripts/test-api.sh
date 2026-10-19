#!/bin/sh
# Set API_URL explicitly to test a different running API. This creates one task.
set -eu
exec python3 "$(dirname "$0")/../smoke_api.py"
