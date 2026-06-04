import json
import os
import requests
import yaml
from pathlib import Path

WATCHLIST = "config/watchlist.yml"
DATABASE = "data/notified.json"

with open(WATCHLIST, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

Path("data").mkdir(exist_ok=True)

if os.path.exists(DATABASE):
    with open(DATABASE, "r") as f:
        notified = set(json.load(f))
else:
    notified = set()

token = os.environ["GITHUB_TOKEN"]
webhook = os.environ["DISCORD_WEBHOOK_URL"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

new_ids = set()

for item in config["repos"]:
    repo = item["repo"]

    for label in item["labels"]:

        q = f'repo:{repo} label:"{label}" state:open'

        r = requests.get(
            "https://api.github.com/search/issues",
            params={"q": q},
            headers=headers,
            timeout=30
        )

        r.raise_for_status()

        issues = r.json()["items"]
        print("Loading watchlist...")
        print("=" * 50)
        print("Repo:", repo)
        print("Label:", label)
        print("Found:", len(issues))
        
        for issue in issues:

            issue_id = issue["id"]

            new_ids.add(issue_id)

            if issue_id in notified:
                print("Already notified:", issue["title"])
                continue

            msg = {
                "content":
                f"🆕 New Issue\n\n"
                f"**{issue['title']}**\n"
                f"Repo: {repo}\n"
                f"Label: {label}\n"
                f"{issue['html_url']}"
            }

            resp = requests.post(
                webhook,
                json=msg,
                timeout=30
            )
            
            print(
                "Discord:",
                resp.status_code,
                issue["title"]
            )

            print("Notify:", issue["title"])

notified.update(new_ids)

with open(DATABASE, "w") as f:
    json.dump(sorted(notified), f)
