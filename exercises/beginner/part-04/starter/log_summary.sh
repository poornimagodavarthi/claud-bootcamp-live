#!/usr/bin/env bash
set -euo pipefail

# Print a one-line summary of every .log file in the current directory.
for f in *.log; do
  if [ ! -e "$f" ]; then
    echo "No .log files here." >&2
    exit 0
  fi
  lines=$(wc -l < "$f")
  bytes=$(wc -c < "$f")
  echo "$f: $lines lines, $bytes bytes"
done
