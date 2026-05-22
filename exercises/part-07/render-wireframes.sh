#!/usr/bin/env bash
# Render wireframe sources to PNG.
# Run from exercises/part-07/.
#
# Outputs:
#   wireframe.png         (from wireframe.mmd via mermaid-cli)
#   wireframe-sketch.png  (from wireframe-sketch.svg via resvg-js)

set -euo pipefail

cd "$(dirname "$0")"

echo "==> Rendering wireframe.mmd → wireframe.png (1280x720)"
npx -y @mermaid-js/mermaid-cli -i wireframe.mmd -o wireframe.png -w 1280 -H 720

echo "==> Rendering wireframe-sketch.svg → wireframe-sketch.png"
# resvg-js is a JS API; fall back to rsvg-convert if available.
if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w 1280 -h 720 wireframe-sketch.svg -o wireframe-sketch.png
else
  npx -y @resvg/resvg-js wireframe-sketch.svg wireframe-sketch.png 2>/dev/null || {
    echo "  (resvg-js entry-point varies; if this fails install librsvg: 'brew install librsvg' then re-run.)"
    exit 1
  }
fi

echo "==> Done."
ls -la wireframe.png wireframe-sketch.png
