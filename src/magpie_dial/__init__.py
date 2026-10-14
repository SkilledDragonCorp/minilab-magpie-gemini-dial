"""Magpie Gemini dial: profile validation and keyless failover stub."""

from magpie_dial.failover import FailoverStub, next_member
from magpie_dial.profile import ProfileError, load_profile, validate_profile

__all__ = [
    "FailoverStub",
    "ProfileError",
    "load_profile",
    "next_member",
    "validate_profile",
]

__version__ = "0.1.0"
