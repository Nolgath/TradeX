from playwright.sync_api import sync_playwright
import time
import pandas as pd

# df = pd.read_excel('vins.xlsx')
#
# vins = df['VIN'].tolist()
# regs = df['First Reg'].tolist()
# mileages = [int(round(x)) for x in df['Mileage']]

#0005/CZT
#14.07.2021
#20000

vins = ['ZARNASAS2N3024410']
regs = ['10.05.2023']
mileages = ['69084']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://de.schwacke.de/auth/login")

    page.wait_for_selector("#ccc-recommended-settings")
    page.click("#ccc-recommended-settings")

    # login
    page.fill('input[placeholder="Mailadresse eingeben"]', "ak@auto-mega-store.com")
    page.fill('input[placeholder="Passwort eingeben"]', "Automegastore1$")
    page.click('button[type="submit"]')

    page.wait_for_selector('button:has-text("Ja")')
    page.click('button:has-text("Ja")')

    for vin, reg, km in zip(vins, regs, mileages):
        time.sleep(1)
        page.fill('input[placeholder="VIN eingeben"]', vin)
        time.sleep(1)

        # Open calendar
        page.click('input[placeholder="Datum auswählen"]')
        page.keyboard.type(reg)  # type date manually
        page.keyboard.press("Enter")  # confirm in picker

        time.sleep(1)
        page.fill('input[placeholder="Zahl eingeben"]', str(km))
        page.keyboard.press("Enter")
        page.click("body")
        time.sleep(1)
        page.wait_for_selector('button:has-text("Suche")')
        page.click('button:has-text("Suche")')

        page.wait_for_load_state("networkidle")
        time.sleep(1)

        rows = page.query_selector_all('div.ag-center-cols-container .ag-row')
        page.locator('div[role="row"][row-id="0"]').click()


    time.sleep(5)
    browser.close()


#Scrapes

#Price ->


# if "Mehrfach gestartete Bewertungen" in page.content():
#     if page.locator("span.item-title").count() > 0:
#         page.locator("span.item-title").first.click()
#         print(vin, "Opened from duplicate list")
#     else:
#         continue
# # else just continues automatically


# price_text = page.locator('#avTradeInPrice').inner_text().strip()
# print(vin,'|', reg,'|', km, '|',price_text)
# page.goto('https://de.schwacke.de/')