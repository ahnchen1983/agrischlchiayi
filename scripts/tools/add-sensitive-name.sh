#!/usr/bin/env bash
# ============================================================
# Register new sensitive identifier(s) with the deidentification hook
# ============================================================
# Thin wrapper that delegates to the Python implementation.
# Names are passed as CLI arguments and never written to disk;
# only their SHA256-16 hashes are persisted.
#
# Usage:
#   bash scripts/tools/add-sensitive-name.sh "姓名1" ["姓名2" ...]
# ============================================================

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/add-sensitive-name.py" "$@"
