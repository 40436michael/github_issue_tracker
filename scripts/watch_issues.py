import json
import os
import time
from pathlib import Path

import requests
import yaml

WATCHLIST = "config/watchlist.yml"
DATABASE = "data/notified.json"

print("Loading watchlist...", flush=True)
with open(WATCHLIST, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

Path("data").mkdir(exist_ok=True)

if os.path.exists(DATABASE):
    with open(DATABASE, "r", encoding="utf-8") as f:
        notified = set(json.load(f))
else:
    notified = set()

token = os.environ["GITHUB_TOKEN"]
webhook = os.environ["DISCORD_WEBHOOK_URL"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
}


def send_discord(content):
    """Send a message to Discord; retry once if rate-limited. Returns True on success."""
    for _ in range(2):
        resp = requests.post(webhook, json={"content": content}, timeout=30)
        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after", 1)
            time.sleep(float(retry_after))
            continue
        resp.raise_for_status()
        return True
    return False


for item in config["repos"]:
    repo = item["repo"]

    for label in item["labels"]:
        print("=" * 50)
        print("Repo:", repo)
        print("Label:", label)

        q = f'repo:{repo} label:"{label}" state:open'

        try:
            r = requests.get(
                "https://api.github.com/search/issues",
                params={"q": q},
                headers=headers,
                timeout=30,
            )
            r.raise_for_status()
        except requests.RequestException as e:
            body = getattr(e.response, "text", "")
            print(f"Failed for {repo} / {label}: {e}\n{body}", flush=True)
            continue

        issues = r.json()["items"]
        print("Found:", len(issues))

        for issue in issues:
            issue_id = issue["id"]

            if issue_id in notified:
                print("Already notified:", issue["title"])
                continue

            content = (
                f"🆕 New Issue\n\n"
                f"**{issue['title']}**\n"
                f"Repo: {repo}\n"
                f"Label: {label}\n"
                f"{issue['html_url']}"
            )

            try:
                ok = send_discord(content)
            except requests.RequestException as e:
                print("Discord failed:", issue["title"], e, flush=True)
                continue

            if not ok:
                print("Discord rate-limited, skipped:", issue["title"], flush=True)
                continue

            notified.add(issue_id)
            print("Notify:", issue["title"])

with open(DATABASE, "w", encoding="utf-8") as f:
    json.dump(sorted(notified), f)

print("Done.", flush=True)
