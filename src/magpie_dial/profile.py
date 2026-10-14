"""Validate a Magpie dial profile YAML for Gemini CLI routing (no network)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REQUIRED_TOP = ("name", "privacy", "agents", "failover")
REQUIRED_PRIVACY = ("magpie_no_accounts",)
REQUIRED_GEMINI = ("route", "auth", "model", "base_url")
REQUIRED_FAILOVER = ("group", "strategy", "members")
ALLOWED_STRATEGIES = frozenset({"next", "pace", "round-robin"})
ALLOWED_AUTH = frozenset({"gemini-api-key", "google", "vertex"})


class ProfileError(ValueError):
    """Profile YAML failed structural validation."""


def load_profile(path: Path | str) -> dict[str, Any]:
    """Load YAML from disk and return the parsed mapping."""
    text = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ProfileError("profile root must be a mapping")
    return data


def validate_profile(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a Magpie Gemini dial profile.

    Requires MAGPIE_NO_ACCOUNTS privacy flag, a Gemini CLI agent routed through
    Magpie, and a non-empty failover group. Does not call any network API.
    """
    for key in REQUIRED_TOP:
        if key not in data:
            raise ProfileError(f"missing top-level key: {key}")

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ProfileError("name must be a non-empty string")

    privacy = data["privacy"]
    if not isinstance(privacy, dict):
        raise ProfileError("privacy must be a mapping")
    for key in REQUIRED_PRIVACY:
        if key not in privacy:
            raise ProfileError(f"privacy missing key: {key}")
    if privacy["magpie_no_accounts"] is not True:
        raise ProfileError("privacy.magpie_no_accounts must be true")

    agents = data["agents"]
    if not isinstance(agents, dict):
        raise ProfileError("agents must be a mapping")
    if "gemini" not in agents:
        raise ProfileError("agents.gemini is required")
    gemini = agents["gemini"]
    if not isinstance(gemini, dict):
        raise ProfileError("agents.gemini must be a mapping")
    for key in REQUIRED_GEMINI:
        if key not in gemini:
            raise ProfileError(f"agents.gemini missing key: {key}")
    if gemini["route"] != "magpie":
        raise ProfileError("agents.gemini.route must be 'magpie'")
    if gemini["auth"] not in ALLOWED_AUTH:
        raise ProfileError(f"agents.gemini.auth must be one of {sorted(ALLOWED_AUTH)}")
    model = gemini["model"]
    if not isinstance(model, str) or "/" not in model:
        raise ProfileError("agents.gemini.model must be 'provider/model'")
    base_url = gemini["base_url"]
    if not isinstance(base_url, str) or not base_url.startswith("http"):
        raise ProfileError("agents.gemini.base_url must be an http(s) URL")

    failover = data["failover"]
    if not isinstance(failover, dict):
        raise ProfileError("failover must be a mapping")
    for key in REQUIRED_FAILOVER:
        if key not in failover:
            raise ProfileError(f"failover missing key: {key}")
    if not isinstance(failover["group"], str) or not failover["group"].strip():
        raise ProfileError("failover.group must be a non-empty string")
    if failover["strategy"] not in ALLOWED_STRATEGIES:
        raise ProfileError(f"failover.strategy must be one of {sorted(ALLOWED_STRATEGIES)}")
    members = failover["members"]
    if not isinstance(members, list) or len(members) < 2:
        raise ProfileError("failover.members must be a list of at least 2 models")
    for i, member in enumerate(members):
        if not isinstance(member, str) or "/" not in member:
            raise ProfileError(f"failover.members[{i}] must be 'provider/model'")

    return data
