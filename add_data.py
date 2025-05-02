from playwright.sync_api import sync_playwright
from faker import Faker
import json

# Faker is used to generate fake usernames/emails
fake = Faker()

# Atlassian Admin URL with specific organization ID
ORG_URL = "https://admin.atlassian.com/o/be0df05b-77ec-4a4f-ac84-f818bef651ce/"

def create_groups_and_users():
     # Launch Playwright browser and load session from saved login state
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        # Step 1: Create 25 groups
        print("creating 25 groups")
        page.goto(ORG_URL + "groups", timeout=60000)
        for i in range(3,26):
            group_name = f"test_group_{i}"
            try:
                page.click("text=Create group", force=True)
                group_input = page.get_by_label("Group's name*", exact=True)
                group_input.wait_for(timeout=10000)
                group_input.fill(group_name)
                page.get_by_test_id("test-create-group-modal-button").click()
                page.wait_for_timeout(1000)
                # Navigate again to refresh the groups list
                page.goto(ORG_URL + "groups", timeout=2000)

            except Exception as e:
                print(f"error creating group {group_name} : {e}")

        # Step 2: Create users (via invite)
        print("creating users")
        page.goto(ORG_URL + "users", timeout=60000)
        for i in range(1,20):
            email = f"{fake.user_name()}@artificial.com"
            try:
                page.click("text=Invite users", force=True)
                user_input = page.get_by_label("Email addresses", exact=True)
                user_input.wait_for(timeout=10000)
                user_input.fill(email)
                user_input.press("Enter")
                page.wait_for_timeout(2000)
                page.mouse.click(10, 10)    # Clicking outside to enable "Invite" button    
                page.get_by_test_id("invite-submit-button").click()
                page.wait_for_timeout(1000)
                print(f"created user {email}")
                
            except Exception as e:
                print(f"error creating user {email} : {e}")

        browser.close()


# Generates a list of fake email addresses using Faker
def generate_emails(domain="debugger.com", count=15):
    return [f"{fake.user_name()}@{domain}" for _ in range(count)]

def create_users():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="state.json")  # Ensure you're logged in
        page = context.new_page()

        page.goto(ORG_URL + "users", timeout=60000)

        # Generate emails
        emails = generate_emails()
        email_string = ", ".join(emails)
        print("Generated Emails:", email_string)

        # Open "Invite users" modal
        page.click("text=Invite users", force=True)

        # Fill in email addresses
        user_input = page.get_by_label("Email addresses", exact=True)
        user_input.wait_for(timeout=10000)
        user_input.fill(email_string)

        # Click outside the field to trigger invite button
        page.mouse.click(110, 100)

        # Submit the invite
        page.get_by_test_id("invite-submit-button").click()

        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    create_users()
