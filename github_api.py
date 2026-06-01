import requests


def fetch_issues(repo, label):
    url = f"https://api.github.com/repos/{repo}/issues"

    params = {
        "state": "open",
        "labels": label,
        "per_page": 100   # 🔥 改 100（避免漏資料）
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, params=params, headers=headers)

    if r.status_code != 200:
        print(f"[ERROR] {repo} {label}: {r.status_code}")
        return []

    return r.json()