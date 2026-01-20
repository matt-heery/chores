"""Test tasks functionality."""

import os

import pytest

import tasks


def test_get_tasks_by_assignee(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test getting tasks grouped by assignee."""
    os.environ["TODOIST_API_TOKEN"] = "TEST_TOKEN"  # noqa: S105

    fake_projects = [
        {
            "id": "proj_1",
            "name": "House Chores",
            "url": "https://todoist.com/app/project/123",
        }
    ]

    fake_tasks = [
        {"id": "1", "content": "Take out trash", "assignee_id": "user_1"},
        {"id": "2", "content": "Clean bathroom", "assignee_id": "user_2"},
        {"id": "3", "content": "Vacuum", "assignee_id": "user_1"},
        {"id": "4", "content": "Unassigned task"},
    ]

    class FakeResponse:
        def __init__(self, json_data: str) -> None:
            """Initialize fake response."""
            self._json = json_data

        def json(self) -> str:
            return self._json

    def fake_get(
        url: str, headers: str | None = None, params: str | None = None, timeout: int | None = None
    ) -> FakeResponse:
        """Fake requests.get method."""
        assert headers == {"Authorization": "Bearer TEST_TOKEN"}
        assert timeout == 100  # noqa: PLR2004

        if url.endswith("/projects"):
            return FakeResponse(fake_projects)

        if url.endswith("/tasks"):
            assert params == {"project_id": "proj_1"}
            return FakeResponse(fake_tasks)

        msg = f"Unexpected URL: {url}"
        raise AssertionError(msg)

    monkeypatch.setattr(tasks.requests, "get", fake_get)

    grouped, project_url = tasks.get_tasks_by_assignee()

    assert project_url == "https://todoist.com/app/project/123"

    assert grouped == {
        "user_1": ["Take out trash", "Vacuum"],
        "user_2": ["Clean bathroom"],
    }
