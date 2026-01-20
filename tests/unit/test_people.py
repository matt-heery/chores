"""Test people module."""

import pytest

import people


def test_get_user_whatsapp_map(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test getting user to whatsapp mapping."""
    monkeypatch.setenv("TODOIST_USER_MAP", '{"user_1": "ALEX", "user_2": "SAM", "user_3": "MISSING"}')

    monkeypatch.setenv("WA_ALEX", "whatsapp:+111111111")
    monkeypatch.setenv("WA_SAM", "whatsapp:+222222222")

    result = people.get_user_whatsapp_map()

    assert result == {
        "user_1": "whatsapp:+111111111",
        "user_2": "whatsapp:+222222222",
    }
