from __future__ import annotations

import pytest

from magpie_dial.failover import FailoverStub, next_member

MEMBERS = ["google/gemini-2.5-flash", "google/gemini-2.5-pro"]


def test_next_member_after_quota() -> None:
    assert next_member(MEMBERS, exhausted_index=0) == "google/gemini-2.5-pro"


def test_stub_advances_and_raises_when_all_exhausted() -> None:
    stub = FailoverStub(members=list(MEMBERS), strategy="next")
    assert stub.current == "google/gemini-2.5-flash"
    assert stub.mark_quota_exhausted() == "google/gemini-2.5-pro"
    with pytest.raises(RuntimeError, match="exhausted"):
        stub.mark_quota_exhausted()


def test_stub_requires_two_members() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        FailoverStub(members=["only-one"])
