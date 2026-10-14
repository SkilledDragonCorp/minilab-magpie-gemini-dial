"""Keyless quota-failover stub (no live API calls)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FailoverStub:
    """In-memory routing group that advances on quota exhaustion."""

    members: list[str]
    strategy: str = "next"
    index: int = 0
    exhausted: set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        if len(self.members) < 2:
            raise ValueError("failover needs at least 2 members")
        if self.strategy not in {"next", "pace", "round-robin"}:
            raise ValueError(f"unknown strategy: {self.strategy}")

    @property
    def current(self) -> str:
        return self.members[self.index]

    def mark_quota_exhausted(self, member: str | None = None) -> str:
        """
        Mark the active (or named) member exhausted and return the next member.

        Raises RuntimeError when every member is exhausted.
        """
        if member is None:
            idx = self.index
        else:
            try:
                idx = self.members.index(member)
            except ValueError as exc:
                raise ValueError(f"unknown member: {member}") from exc
        self.exhausted.add(idx)
        return self._advance()

    def _advance(self) -> str:
        n = len(self.members)
        for offset in range(1, n + 1):
            cand = (self.index + offset) % n
            if cand not in self.exhausted:
                self.index = cand
                return self.members[cand]
        raise RuntimeError("all failover members exhausted")


def next_member(members: list[str], exhausted_index: int = 0) -> str:
    """Return the next member after ``exhausted_index`` (wraps; keyless helper)."""
    stub = FailoverStub(members=list(members), index=exhausted_index)
    return stub.mark_quota_exhausted()
