#!/usr/bin/env bash
# Verbatim Linux keyless suite from yetone/magpie .github/workflows/test.yml
# at pin e297a8ab27461ed32b03ce8be0f9bf957a2e754d (Linux matrix job).
# Bun 1.4.2 must already be on PATH (CI: oven-sh/setup-bun).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="e297a8ab27461ed32b03ce8be0f9bf957a2e754d"
MAGPIE="$ROOT/vendor/magpie"

export MAGPIE_NO_ACCOUNTS=1
export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1

if [[ ! -d "$MAGPIE/.git" ]]; then
  echo "missing vendor/magpie; run: bash scripts/vendor-upstream.sh" >&2
  exit 1
fi

HEAD="$(git -C "$MAGPIE" rev-parse HEAD)"
if [[ "$HEAD" != "$PIN" ]]; then
  echo "vendor pin mismatch: expected $PIN got $HEAD" >&2
  exit 1
fi

cd "$MAGPIE"

sudo apt-get update
sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.1-dev
# gofmt check (Linux only — Windows CRLF):
bad=$(gofmt -l $(git ls-files '*.go'))
if [ -n "$bad" ]; then echo "not gofmt'd:"; echo "$bad"; exit 1; fi
go vet -tags gtk3 ./...
# bun 1.4.2 via oven-sh/setup-bun@v2 (workflow step) before plugin tests that need bun on PATH
bun --version
go test -tags gtk3 ./...
