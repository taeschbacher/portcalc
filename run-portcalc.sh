#!/usr/bin/env bash
set -euo pipefail

# Build and run portcalc with Python 3.13 via Podman.
# Run this script from anywhere; it will switch to the project root first.

IMAGE_NAME="${IMAGE_NAME:-portcalc:py313}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$PROJECT_ROOT"

mkdir -p data results plots

podman build -t "$IMAGE_NAME" .

podman run --rm \
  -v "$PWD/data:/app/data:Z" \
  -v "$PWD/results:/app/results:Z" \
  -v "$PWD/plots:/app/plots:Z" \
  "$IMAGE_NAME"
