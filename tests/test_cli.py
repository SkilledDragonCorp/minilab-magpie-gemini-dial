from __future__ import annotations

from pathlib import Path

from magpie_dial.cli import main

FIXTURE = Path(__file__).parent / "fixtures" / "gemini-profile.yaml"


def test_cli_ok(capsys) -> None:
    assert main([str(FIXTURE)]) == 0
    out = capsys.readouterr().out
    assert "OK gemini-dial" in out


def test_cli_simulate_failover(capsys) -> None:
    assert main([str(FIXTURE), "--simulate-failover"]) == 0
    out = capsys.readouterr().out
    assert "next=google/gemini-2.5-pro" in out
