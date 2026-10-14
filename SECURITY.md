# Security Policy

**Built by [SkilledDragon LLC](https://skilleddragon.com)**

This is a **SkilledDragon educational minilab**, not a production product. We do **not** maintain these repos on a regular schedule and we do **not** operate a vulnerability response program for them.

## Contact

General questions: **hello@skilleddragon.com**  
Do not use a dedicated security mailbox for this repo — none exists.

## If you find an issue

- Prefer reporting **upstream** when the issue is in [yetone/magpie](https://github.com/yetone/magpie).
- For something specific to this minilab's dial scripts or CI, you may email hello@skilleddragon.com. There is **no SLA**, and we may not patch or reply quickly.

## Supported versions

Only the commit currently on `main` is considered current for this educational lab.

## Secret handling

- Never commit `.env`, API keys, or tokens.
- Secrets are read from environment variables (local `.env`; GitHub Actions secrets in CI).
- CI is keyless. Optional `GEMINI_API_KEY` is for a live dial outside CI only.
- Always set `MAGPIE_NO_ACCOUNTS=1` so Magpie does not discover subscription accounts from agent sign-in files.
- Set `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` for lab runs.

## Tooling pins

| Control | Pin |
| --- | --- |
| Upstream | `yetone/magpie` @ `e297a8ab27461ed32b03ce8be0f9bf957a2e754d` (MIT) |
| gitleaks | `v8.30.1` (pre-commit hook + CI binary with SHA256 verify) |
| Dependency audit | `uv export --frozen --format requirements-txt --no-emit-project > /tmp/req.txt` then `uvx pip-audit --strict -r /tmp/req.txt` |

## Upstream license

`yetone/magpie` is MIT. Use at your own risk. Pin versions, review the code, and treat this as sample material.
