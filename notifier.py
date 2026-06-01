import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

if not DISCORD_WEBHOOK:
    raise RuntimeError("缺少 DISCORD_WEBHOOK")


def send_discord_issue(issue, repo: str, label: str = ""):

    title = issue.get("title", "No title")
    number = issue.get("number", "")
    url = issue.get("html_url", "")

    content = (
        "🔔 **New GitHub Issue Detected**\n"
        f"📦 Repo: `{repo}`\n"
        f"🏷️ Label: `{label}`\n"
        f"🆔 #{number} {title}\n"
        f"🔗 {url}"
    )

    resp = requests.post(
        DISCORD_WEBHOOK,
        json={"content": content}
    )

    if resp.status_code not in (200, 204):
        print(f"[Discord Error] {resp.status_code}: {resp.text}")