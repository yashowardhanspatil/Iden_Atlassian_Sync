from playwright.sync_api import sync_playwright

def login_and_save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://admin.atlassian.com")
        page.wait_for_timeout(60000)
        context.storage_state(path="state.json")
        browser.close()

if __name__ == "__main__":
    login_and_save_session()