---
name: magpie-gemini-dial
description: Route Gemini CLI / Antigravity through Magpie with MAGPIE_NO_ACCOUNTS=1 and validate a quota-failover dial profile (keyless).
---

# Magpie Gemini dial

Local gateway dial for **Gemini CLI** (and Antigravity) through [yetone/magpie](https://github.com/yetone/magpie), with privacy accounts discovery off and a keyless failover stub.

## Privacy (required)

Always export before running Magpie or lab tools:

```bash
export MAGPIE_NO_ACCOUNTS=1
export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1
```

`MAGPIE_NO_ACCOUNTS=1` turns off subscription-account discovery for one run without changing Magpie's saved privacy setting.

## Validate the dial profile (keyless)

From the repository root:

```bash
uv sync --locked --group dev
uv run magpie-dial tests/fixtures/gemini-profile.yaml
uv run magpie-dial tests/fixtures/gemini-profile.yaml --simulate-failover
```

The fixture routes Gemini CLI through Magpie at `http://127.0.0.1:3425` and declares a two-member failover group. CI never calls the Gemini API.

## Quota failover concept

Magpie routing groups move to the next account or model when a quota window is exhausted. This lab's `FailoverStub` models that advance in-process: mark the active member exhausted, receive the next `provider/model`. No live keys required.

## Optional live dial (not CI)

With Magpie running locally and `GEMINI_API_KEY` set in `.env`, point Gemini CLI through the gateway (`GOOGLE_GEMINI_BASE_URL` + gateway token) as documented upstream. Do not commit keys.

## Upstream pin

`vendor/magpie` @ `e297a8ab27461ed32b03ce8be0f9bf957a2e754d` via `bash scripts/vendor-upstream.sh`. Linux keyless suite: `bash scripts/upstream-magpie.sh` (GTK deps + gofmt/vet/test).
