from config import REPOS, LABELS
from github_api import fetch_issues
from notifier import send_discord_issue
from store import load_seen, save_seen, is_new, mark_seen


def main():
    seen = load_seen()

    for repo in REPOS:
        for label in LABELS:

            issues = fetch_issues(repo, label)

            for issue in issues:

                if "pull_request" in issue:
                    continue

                if is_new(issue, repo, seen):
                    send_discord_issue(issue, repo, label)
                    mark_seen(issue, repo, seen)

    save_seen(seen)


if __name__ == "__main__":
    main()