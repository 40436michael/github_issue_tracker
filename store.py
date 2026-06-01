import json
import os

FILE = "seen.json"


def load_seen():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_seen(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_new(issue, repo, seen):
    repo_seen = seen.get(repo, [])
    return issue["number"] not in repo_seen


def mark_seen(issue, repo, seen):
    seen.setdefault(repo, [])
    seen[repo].append(issue["number"])