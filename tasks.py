"""Get tasks from Todoist and group them by assignee."""

import os
from collections import defaultdict

import requests

TODOIST_API = "https://api.todoist.com/rest/v2"
PROJECT_NAME = "House Chores"


def get_tasks_by_assignee() -> tuple[dict[str, list[str]], str]:
    """Get tasks for each member."""
    headers = {"Authorization": f"Bearer {os.environ['TODOIST_API_TOKEN']}"}

    projects = requests.get(f"{TODOIST_API}/projects", headers=headers, timeout=100).json()

    project = next(p for p in projects if p["name"] == PROJECT_NAME)
    project_url = project["url"]

    tasks = requests.get(
        f"{TODOIST_API}/tasks", headers=headers, params={"project_id": project["id"]}, timeout=100
    ).json()

    grouped = defaultdict(list)

    for t in tasks:
        if not t.get("assignee_id"):
            continue

        grouped[t["assignee_id"]].append(t["content"])

    return grouped, project_url
