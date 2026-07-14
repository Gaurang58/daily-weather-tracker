#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

source "$PROJECT_DIR/.venv/bin/activate"

python3 "$PROJECT_DIR/src/collect_weather.py"

git add data/weather.csv

if git diff --cached --quiet; then
    echo "No new weather data to commit."
    exit 0
fi

git commit -m "Record daily weather for $(date '+%Y-%m-%d')"
git push origin main

echo "Daily weather collection completed."