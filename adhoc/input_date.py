import time

from playwright.sync_api import sync_playwright
import pandas as pd

df = pd.read_excel('inputs.xlsx')
ids = df['ID'] = df['ID'].astype(str).str.strip().to_list()
print(ids)

username = 'c.zorila'
password = 'MemoCristian2025'

url = 'https://ams-de.mega-moves.com/portal/vehicles/pages/vehicle-details-4.php?wgID='

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # Login into the page.
    page.goto("https://ams-de.mega-moves.com/")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")

    # Output Date Input:
    for id in ids:
        print(id)
        link = url + id
        page.goto(link)
        time.sleep(1)
        page.eval_on_selector(
            "input[name='Eingang']",
            "el => { el.removeAttribute('readonly'); el.value = ''; el.dispatchEvent(new Event('input')); }"
        )
        page.evaluate("submit('/portal/vehicles/pages/vehicle-details-4.php')")

        time.sleep(2)