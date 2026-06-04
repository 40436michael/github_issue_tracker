# GitHub Issue Tracker

利用 GitHub Actions 自動追蹤指定 GitHub Repository 的 Issue Label（例如 `good first issue`、`help wanted`），並在發現新的符合條件 Issue 時，自動發送 Discord 通知。

## 功能特色

* 自動追蹤多個 GitHub Repository
* 支援多個 Label 條件
* 使用 GitHub Actions 定時執行
* Discord Webhook 即時通知
* 避免重複通知相同 Issue
* 透過設定檔管理追蹤目標
* 無需自行架設伺服器

---

## 專案架構

```text
github_issue_tracker/
│
├── .github/
│   └── workflows/
│       └── watch_issues.yml
│
├── config/
│   └── watchlist.yml
│
├── data/
│   └── notified.json
│
├── scripts/
│   └── watch_issues.py
│
└── README.md
```

---

## 運作流程

```text
GitHub Actions 排程
        │
        ▼
watch_issues.yml
        │
        ▼
watch_issues.py
        │
        ├── 讀取 watchlist.yml
        │
        ├── 查詢 GitHub Search API
        │
        ├── 篩選指定 Label
        │
        ├── 比對 notified.json
        │
        ├── 發送 Discord 通知
        │
        └── 更新 notified.json
```

---

## 設定追蹤目標

編輯：

```text
config/watchlist.yml
```

範例：

```yaml
repos:
  - repo: ankitects/anki
    labels:
      - good first issue
      - help wanted

  - repo: sillytavern/SillyTavern
    labels:
      - good first issue

  - repo: apache/mahout
    labels:
      - good first issue
```

### 說明

* `repo`：GitHub Repository 名稱
* `labels`：欲追蹤的 Label

每個 Repository 可以設定多個 Label。

---

## Discord Webhook 設定

### 建立 Discord Webhook

1. 進入 Discord 伺服器設定
2. 選擇「整合」
3. 建立 Webhook
4. 複製 Webhook URL

### 設定 GitHub Secret

進入：

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
```

新增：

| Secret 名稱           | 說明                  |
| ------------------- | ------------------- |
| DISCORD_WEBHOOK_URL | Discord Webhook URL |

---

## GitHub Actions 排程

目前設定：

```yaml
schedule:
  - cron: "*/30 * * * *"
```

代表：

```text
每 30 分鐘執行一次
```

執行時間範例：

```text
00:00
00:30
01:00
01:30
02:00
...
```

### 常用排程設定

| Cron         | 說明       |
| ------------ | -------- |
| */30 * * * * | 每 30 分鐘  |
| 0 * * * *    | 每小時      |
| 0 */6 * * *  | 每 6 小時   |
| 0 0 * * *    | 每天凌晨 0 點 |
| 0 8 * * *    | 每天早上 8 點 |

---

## Discord 通知範例

```text
🆕 New Issue

Preview does not update when changing the flag

Repo: ankitects/anki
Label: good first issue

https://github.com/ankitects/anki/issues/xxxxx
```

---

## 防止重複通知機制

系統會將已通知過的 Issue ID 記錄於：

```text
data/notified.json
```

範例：

```json
[
  799988188,
  835874815,
  4439630366
]
```

下次執行時：

```text
若 Issue ID 已存在
↓
不再通知

若為新的 Issue ID
↓
發送 Discord 通知
↓
寫入 notified.json
```

---

## 手動執行

除了排程外，也可手動執行：

```text
Actions
→ Watch Issues
→ Run workflow
```

適合測試設定是否正常。

---

## 使用技術

* GitHub Actions
* Python 3.12
* GitHub Search API
* Discord Webhook
* Requests
* PyYAML

---

## 未來可擴充功能

* Telegram 通知
* Email 通知
* Slack 通知
* 關鍵字篩選
* 指定程式語言標籤
* 每日摘要報告
* Issue 統計儀表板

---


