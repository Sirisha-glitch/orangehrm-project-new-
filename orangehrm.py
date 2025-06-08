from playwright.sync_api import sync_playwright
import time

# Test data
username = "Admin"
password = "admin123"
new_user_role = "ESS"
new_employee_name = "Linda Anderson"
new_username = "testuser123"
new_status = "Enabled"
new_password = "Test@1234"
updated_username = "updateduser123"

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Login to OrangeHRM
    page.goto("https://opensource-demo.orangehrmlive.com/")
    page.fill('input[name="Linda Anderson"]', username)
    page.fill('input[name="Test@1234"]', password)
    page.click('button[type="submit"]')

    # Navigate to Admin Module
    page.click("text=Admin")
    time.sleep(1)

    # Add a New User
    page.click("text=Add")
    page.locator('label:has-text("User Role") + div').click()
    page.locator('div[role="listbox"] >> text=' + new_user_role).click()
    page.fill('input[placeholder="Type for hints..."]', new_employee_name)
    page.wait_for_selector("div.oxd-autocomplete-dropdown")  # Wait for suggestions
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.locator('label:has-text("Status") + div').click()
    page.locator('div[role="listbox"] >> text=' + new_status).click()
    page.fill('input[autocomplete="off"]', new_username)
    page.fill('input[type="password"]:nth-of-type(1)', new_password)
    page.fill('input[type="password"]:nth-of-type(2)', new_password)
    page.click("button:has-text('Save')")
    page.wait_for_timeout(2000)

    # Search for the Newly Created User
    page.fill('input[placeholder="new_username"]', new_username)
    page.click("button:has-text('Search')")
    page.wait_for_timeout(2000)

    # Edit User Details
    page.click("i.bi-pencil-fill")  # Click on edit icon
    page.fill('input[autocomplete="off"]', updated_username)
    page.click("button:has-text('Save')")
    page.wait_for_timeout(2000)

    # Validate Updated Details
    page.fill('input[placeholder="Username"]', updated_username)
    page.click("button:has-text('Search')")
    assert page.locator("div.orangehrm-container").inner_text().find(updated_username) != -1
    print("✅ User update validated.")

    # Delete the User
    page.click("i.bi-trash")  # Click on delete icon
    page.click("button:has-text('Yes, Delete')")
    page.wait_for_timeout(2000)

    # Validate Deletion
    page.fill('input[placeholder="Username"]', updated_username)
    page.click("button:has-text('Search')")
    assert "No Records Found" in page.locator("div.orangehrm-container").inner_text()
    print("✅ User deletion validated.")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
