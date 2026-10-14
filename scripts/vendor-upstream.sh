#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="e297a8ab27461ed32b03ce8be0f9bf957a2e754d"
DEST="$ROOT/vendor/magpie"

mkdir -p "$ROOT/vendor"

if [[ -d "$DEST/.git" ]]; then
  git -C "$DEST" fetch --depth 1 origin "$PIN" || git -C "$DEST" fetch origin "$PIN"
  git -C "$DEST" checkout --force "$PIN"
else
  rm -rf "$DEST"
  git clone https://github.com/yetone/magpie.git "$DEST"
  git -C "$DEST" checkout "$PIN"
fi

HEAD="$(git -C "$DEST" rev-parse HEAD)"
if [[ "$HEAD" != "$PIN" ]]; then
  echo "vendor pin mismatch: expected $PIN got $HEAD" >&2
  exit 1
fi

echo "vendor/magpie @ $HEAD"
