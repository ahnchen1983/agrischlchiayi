#!/usr/bin/env bash
# ============================================================
# Deidentification Pre-commit Check (thin wrapper)
# ============================================================
# Delegates to the Python implementation which uses hash-based
# detection (no cleartext sensitive names stored in this repo).
#
# See scripts/tools/deidentification-check.py for the full logic
# and DEIDENTIFICATION-POLICY.md for the full policy.
# ============================================================

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/deidentification-check.py" "$@"
