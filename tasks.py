"""Get tasks from Todoist."""

import os

import requests

TODOIST_API = "https://api.todoist.com/rest/v2"


def get_weekly_chores() -> str:
    """Get weekly chores from Todoist."""
    headers = {"Authorization": f"Bearer {os.environ['TODOIST_API_TOKEN']}"}

    # Get all projects
    projects = requests.get(f"{TODOIST_API}/projects", headers=headers, timeout=100).json()

    project = next(p for p in projects if p["name"] == "house chores")

    project_id = project["id"]
    project_url = project["url"]

    # Get tasks
    tasks = requests.get(f"{TODOIST_API}/tasks", headers=headers, params={"project_id": project_id}, timeout=100).json()

    chores = [t["content"] for t in tasks]

    if not chores:
        return "🎉 No chores this week!"

    msg = "🧹 *This Week's Chores*\n\n"
    msg += "\n".join(f"• {c}" for c in chores)
    msg += f"\n\n🔗 Open chore board:\n{project_url}"

    return msg
