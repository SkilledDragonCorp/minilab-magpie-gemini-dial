"""CLI: validate a Magpie Gemini dial profile YAML."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from magpie_dial.failover import FailoverStub
from magpie_dial.profile import ProfileError, load_profile, validate_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Magpie Gemini dial profile YAML")
    parser.add_argument("profile", type=Path, help="Path to profile YAML")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print validated profile as JSON",
    )
    parser.add_argument(
        "--simulate-failover",
        action="store_true",
        help="Print next member after marking the first member quota-exhausted",
    )
    args = parser.parse_args(argv)

    try:
        data = validate_profile(load_profile(args.profile))
    except (OSError, ProfileError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.simulate_failover:
        members = list(data["failover"]["members"])
        stub = FailoverStub(members=members, strategy=str(data["failover"]["strategy"]))
        nxt = stub.mark_quota_exhausted()
        print(f"current={stub.members[0]} next={nxt}")

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(f"OK {data['name']} agents.gemini.model={data['agents']['gemini']['model']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
