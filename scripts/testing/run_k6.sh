#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

BASE_URL="${BASE_URL:-${CYPRESS_BASE_URL:-http://127.0.0.1:5050}}"
K6_PROFILE="${K6_PROFILE:-}"
K6_SMOKE="${K6_SMOKE:-}"
K6_VUS="${K6_VUS:-20}"
K6_DURATION="${K6_DURATION:-15s}"
K6_SPIKE_VUS="${K6_SPIKE_VUS:-80}"
K6_SPIKE_RAMP_UP="${K6_SPIKE_RAMP_UP:-10s}"
K6_SPIKE_HOLD="${K6_SPIKE_HOLD:-20s}"
K6_SPIKE_RAMP_DOWN="${K6_SPIKE_RAMP_DOWN:-10s}"
K6_SOAK_VUS="${K6_SOAK_VUS:-25}"
K6_SOAK_DURATION="${K6_SOAK_DURATION:-10m}"

if [ -z "$K6_PROFILE" ]; then
  if [ -n "$K6_SMOKE" ]; then
    if [ "$K6_SMOKE" = "1" ]; then
      K6_PROFILE="smoke"
    else
      K6_PROFILE="load"
    fi
  else
    K6_PROFILE="smoke"
  fi
fi

if ! command -v k6 >/dev/null 2>&1; then
  echo "k6 is not installed or not available on PATH" >&2
  exit 1
fi

exec env \
  BASE_URL="$BASE_URL" \
  QA_K6_PROFILE="$K6_PROFILE" \
  QA_K6_SMOKE_VUS="$K6_VUS" \
  QA_K6_SMOKE_DURATION="$K6_DURATION" \
  QA_K6_SPIKE_VUS="$K6_SPIKE_VUS" \
  QA_K6_SPIKE_RAMP_UP="$K6_SPIKE_RAMP_UP" \
  QA_K6_SPIKE_HOLD="$K6_SPIKE_HOLD" \
  QA_K6_SPIKE_RAMP_DOWN="$K6_SPIKE_RAMP_DOWN" \
  QA_K6_SOAK_VUS="$K6_SOAK_VUS" \
  QA_K6_SOAK_DURATION="$K6_SOAK_DURATION" \
  k6 run load/k6-production-readiness.js
