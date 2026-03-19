#!/bin/bash
set -euo pipefail

# Run a focused regression check for spread neighborhood radius.
# $1 is the binary suffix (same convention as test/test.sh).

BIN="../Cell2Fire/Cell2Fire$1"
if [ ! -x "$BIN" ]; then
  echo "Binary not found or not executable: $BIN"
  exit 1
fi

WORKDIR="spreadrad_test_results"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

run_case () {
  local label="$1"
  local spread_arg="$2"
  local out="$WORKDIR/$label"
  mkdir -p "$out"
  # Keep this short but deterministic.
  "$BIN" \
    --input-instance-folder model/kitral-asc \
    --output-folder "$out" \
    --nsims 30 \
    --max-fire-periods 60 \
    --sim K \
    --seed 123 \
    --ignitionsLog \
    $spread_arg > "$WORKDIR/$label.log"
}

extract_burned () {
  local logfile="$1"
  grep "Total Burnt Cells:" "$logfile" | tail -n1 | sed -E 's/.*Total Burnt Cells:[[:space:]]*([0-9]+).*/\1/'
}

run_case "default" ""
run_case "spread1" "--SpreadRad 1"
run_case "spread2" "--SpreadRad 2"

B_DEFAULT="$(extract_burned "$WORKDIR/default.log")"
B_SPREAD1="$(extract_burned "$WORKDIR/spread1.log")"
B_SPREAD2="$(extract_burned "$WORKDIR/spread2.log")"

if [ -z "$B_DEFAULT" ] || [ -z "$B_SPREAD1" ] || [ -z "$B_SPREAD2" ]; then
  echo "Failed to parse burned-cell counts from logs"
  exit 1
fi

if [ "$B_DEFAULT" != "$B_SPREAD1" ]; then
  echo "SpreadRad regression failed: default burned=$B_DEFAULT, spread1 burned=$B_SPREAD1"
  exit 1
fi

if ! grep -q "SpreadRadius: 2" "$WORKDIR/spread2.log"; then
  echo "SpreadRad=2 run did not report SpreadRadius in output"
  exit 1
fi

# Usually radius 2 burns at least as many cells as radius 1 for this fixed case.
if [ "$B_SPREAD2" -lt "$B_SPREAD1" ]; then
  echo "Unexpected spread result: spread2 burned=$B_SPREAD2 < spread1 burned=$B_SPREAD1"
  exit 1
fi

echo "SpreadRad test passed: default=$B_DEFAULT spread1=$B_SPREAD1 spread2=$B_SPREAD2"
rm -rf "$WORKDIR"
