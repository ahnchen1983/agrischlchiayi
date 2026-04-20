#!/usr/bin/env bash
# ============================================================
# Deidentify raw farmer data — thin wrapper around the Python
# implementation. See scripts/tools/deidentify-source.py for
# the full documentation.
#
# Usage:
#   bash scripts/tools/deidentify-source.sh
# ============================================================

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/deidentify-source.py" "$@"
