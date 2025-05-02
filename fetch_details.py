from playwright.sync_api import sync_playwright
import json
import time

# Atlassian Org ID and base admin URL
ORG_ID = "be0df05b-77ec-4a4f-ac84-f818bef651ce"
BASE_URL = f"https://admin.atlassian.com/o/{ORG_ID}/"

# Fetch all users and their group memberships
def fetch_users_w_grps():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Load authenticated browser context from saved session
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        # Navigate to users page to ensure session and trigger backend readiness
        page.goto(f"{BASE_URL}users", timeout=60000)
        page.wait_for_timeout(5000)
        print("Fetching users...")

        users = []
        start_index = 1
        count = 20

        # Paginate through users API until all are fetched
        while True:
            response = context.request.get(
                f"https://admin.atlassian.com/gateway/api/adminhub/um/org/{ORG_ID}/users?count={count}&start-index={start_index}&status=active"
            )
            if response.status != 200:
                print(f"Error fetching users: {response.status}")
                break

            data = response.json()
            batch = data.get("users", [])
            if not batch:
                break  # No more users to fetch

            users.extend(batch)
            print(f"Fetched {len(users)} users so far...")
            start_index += count
            
            print(f"Total users fetched: {len(users)}")

        # Fetch group memberships for each user
        print("Fetching group memberships for each user...")
        filtered_users = []
        for i, user in enumerate(users):
            user_id = user.get("id")
            email = user.get("email", "")
            name = user.get("displayName", "")
            last_active = user.get("created", "")
            status = user.get("activeStatus", "")

             # Request groups for this specific user
            group_resp = context.request.get(
                f"https://admin.atlassian.com/gateway/api/adminhub/um/org/{ORG_ID}/users/{user_id}/groups?count=20&start-index=1"
            )

            if group_resp.status != 200:
                print(f"Failed to fetch groups for user {user_id}: {group_resp.status}")
                user["groups"] = []
                continue

            group_data = group_resp.json()

            # Extract group names only
            groups = [g.get("name") for g in group_data.get("groups", []) if "name" in g]
            
            # Create filtered user object with only required fields
            filtered_users.append({
                "id": user_id,
                "name": name,
                "email": email,
                "last_active": last_active,
                "status": status,
                "groups": groups
            })

        # Write filtered user data to JSON
        with open("users.json", "w") as f:
            json.dump(filtered_users, f, indent=4)

        print("Done. Data saved to .json")
        browser.close()

# Fetch all groups and store only id, name, and description
def fetch_groups():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Use saved authenticated session
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        # Navigate to groups page to ensure readiness
        page.goto(f"{BASE_URL}groups", timeout=60000)
        page.wait_for_timeout(5000)
        print("Fetching groups...")

        groups = []
        start_index = 1
        count = 20

        # Paginate through group list
        while True:
            response = context.request.get(
                f"https://admin.atlassian.com/gateway/api/adminhub/um/org/{ORG_ID}/groups?count={count}&start-index={start_index}"
            )
            if response.status != 200:
                print(f"Error fetching groups: {response.status}")
                break

            data = response.json()
            batch = data.get("groups", [])
            if not batch:
                break

            groups.extend(batch)
            print(f"Fetched {len(groups)} groups so far...")
            start_index += count

        # Filter and simplify group data
        filtered_groups = []
        for g in groups:
            group_info = {
                "id": g.get("id"),
                "name": g.get("name"),
                "description": g.get("description", "")
            }
            filtered_groups.append(group_info)

        # Write filtered group data to JSON
        with open("groups.json", "w") as f:
            json.dump(filtered_groups, f, indent=4)

        print(f"Total groups fetched: {len(groups)}")
        browser.close()

# Main execution block
if __name__ == "__main__":
    fetch_users_w_grps()        # Fetch users with their group memberships
    time.sleep(2)
    fetch_groups()              # Fetch groups
    time.sleep(2)