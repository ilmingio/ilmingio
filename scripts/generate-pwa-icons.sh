#!/usr/bin/env bash
# Regenerate PNG favicons / PWA icons from ilming_icon.svg
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ICON="$ROOT/assets/images/logo/ilming_icon.svg"
OUT="$ROOT/assets/images/favicon"

render() {
  npx --yes @resvg/resvg-js-cli --fit-width "$1" --fit-height "$1" "$ICON" "$2"
}

render 512 "$OUT/icon-512.png"
render 192 "$OUT/icon-192.png"
render 180 "$OUT/apple-touch-icon.png"
render 96  "$OUT/favicon-96x96.png"
render 32  "$OUT/favicon-32x32.png"
render 16  "$OUT/favicon-16x16.png"

if python3 -c "from PIL import Image" 2>/dev/null; then
  python3 - <<'PY'
from PIL import Image
img = Image.open("assets/images/favicon/favicon-32x32.png")
img.save("assets/images/favicon/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)])
PY
else
  cp "$OUT/favicon-32x32.png" "$OUT/favicon.ico"
fi

echo "PWA icons written to $OUT"
