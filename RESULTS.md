# Results

Local ship gate recorded **2026-10-14 03:00 UTC** (keyless lab suite). Upstream GTK suite runs on Linux CI.

- Python `3.14.7` · `ruff 0.17.0` · `pytest 9.1.1`
- Upstream pin `e297a8ab27461ed32b03ce8be0f9bf957a2e754d`
- `pip-audit --strict`: no known vulnerabilities

| Check | Result | Note |
| --- | --- | --- |
| `uv sync --locked --group dev` | **pass** | Checked 17 packages |
| `uv run ruff check .` | **pass** | All checks passed |
| `uv run ruff format --check .` | **pass** | 11 files already formatted |
| `uv run pytest -q` | **pass** | 10 passed in 0.08s |
| `python3 scripts/check-skills` | **pass** | skills-layout OK |
| `python3 scripts/check-banned-phrases` | **pass** | banned-phrases OK |
| `python3 scripts/check-upstream-parity` | **pass** | upstream-parity OK |

Pytest: **10 passed**.

Upstream `scripts/upstream-magpie.sh`: Linux CI only (GTK/WebKit apt packages).
