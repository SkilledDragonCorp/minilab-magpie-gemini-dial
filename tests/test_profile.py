from __future__ import annotations

from pathlib import Path

import pytest

from magpie_dial.profile import ProfileError, load_profile, validate_profile

FIXTURE = Path(__file__).parent / "fixtures" / "gemini-profile.yaml"


def test_fixture_loads_and_validates() -> None:
    data = validate_profile(load_profile(FIXTURE))
    assert data["name"] == "gemini-dial"
    assert data["privacy"]["magpie_no_accounts"] is True
    assert data["agents"]["gemini"]["route"] == "magpie"
    assert data["agents"]["gemini"]["model"] == "google/gemini-2.5-flash"
    assert len(data["failover"]["members"]) >= 2


def test_rejects_accounts_discovery_on() -> None:
    data = load_profile(FIXTURE)
    data["privacy"]["magpie_no_accounts"] = False
    with pytest.raises(ProfileError, match="magpie_no_accounts"):
        validate_profile(data)


def test_rejects_missing_gemini_agent() -> None:
    data = load_profile(FIXTURE)
    del data["agents"]["gemini"]
    with pytest.raises(ProfileError, match="agents.gemini"):
        validate_profile(data)


def test_rejects_single_failover_member() -> None:
    data = load_profile(FIXTURE)
    data["failover"]["members"] = ["google/gemini-2.5-flash"]
    with pytest.raises(ProfileError, match="at least 2"):
        validate_profile(data)


def test_rejects_non_magpie_route() -> None:
    data = load_profile(FIXTURE)
    data["agents"]["gemini"]["route"] = "direct"
    with pytest.raises(ProfileError, match="route"):
        validate_profile(data)
