# Atlassian Admin Automation

This project automates administrative tasks in the Atlassian Admin Hub using [Playwright](https://playwright.dev/). It performs the following key operations:

* Fetch all **users** with their **group memberships**
* Fetch all **groups** with basic metadata
* Create **new groups** in bulk
* Invite **new users** individually or in bulk
* Uses saved authentication state for secure login bypass

---

## Project Structure

| File            | Description                                         |
| --------------- | --------------------------------------------------- |
| `auth.py`       |Script for logging in and saving session  |
| `add_data.py`       | Automates group creation and user invitation via UI |
| `fetch_details.py` | Fetches all users and groups via Atlassian APIs     |
| `state.json`    | Saved authenticated session from manual login       |
| `users.json`    | Output file: user details + group memberships       |
| `groups.json`   | Output file: group metadata                         |

---

## Setup & Usage

### 1. Install Dependencies

```bash
pip install playwright faker
playwright install
```

### 2. Log in and Save Session

Before using the scripts, log in manually and save the authenticated session:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://admin.atlassian.com")
    input("Login manually and press Enter...")
    context.storage_state(path="state.json")
    browser.close()
```

This will save your login session to `state.json`.

---

### 3. Fetch Users and Groups

Run this to generate `users.json` and `groups.json`:

```bash
python fetch_data.py
```

---

### 4. Create Users & Groups

Run this to create groups and invite users:

```bash
python main.py
```

> You can customize the number of groups and users to be created in the script.

---

##  Sample Output

### `users.json`

```json
[
  {
    "id": "1234abcd",
    "name": "John Doe",
    "email": "john@company.com",
    "last_active": "2025-05-01T08:02:54.062207Z",
    "status": "ENABLED",
    "groups": ["engineering", "admin"]
  }
]
```

### `groups.json`

```json
[
  {
    "id": "group123",
    "name": "engineering",
    "description": "Engineering team members"
  }
]
```

---

## Tech Stack

* **Playwright (Python)** – UI and API automation
* **Faker** – Fake data generation for test users
* **JSON** – Output persistence

---
