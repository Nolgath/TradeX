from playwright.sync_api import sync_playwright,TimeoutError
import time
import pandas as pd

df = pd.read_excel('vins.xlsx')
VIN = df['VIN'].tolist()
brands = df['brand'].tolist()

id = "de-800610"
username = "Admin-PT"
password = "trAdEx2025*!"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.partslink24.com/")
    page.fill("#login-name", username)
    page.fill("#inputPassword", password)
    page.fill('#login-id', id)
    page.keyboard.press("Enter")

    #click by text
    page.locator("[data-testid='uc-accept-all-button']").click()
    time.sleep(1)
    page.locator("#squeezeout-login-btn").click()
    time.sleep(1)

    page.goto('https://www.partslink24.com/fiatspa/fiatp_parts/vehicle.action?mode=A0LU0DEDE&lang=en&startup=true&upds=2025.11.12+15%3A53%3A23+CET')

    number_of_vins = len(VIN)
    vins_extracted = 0

    data = []  # final dictionary

    BATCH_SIZE = 30

    for vin, brand in zip(VIN, brands):
        print(f'{vin} : {vins_extracted}/{number_of_vins}')
        page.fill("#vin", vin)
        page.keyboard.press("Enter")

        try:
            page.locator("a[href='#vinStandardEquipment']").click()
        except TimeoutError:
            print(f'No equipment found for {vin}')
            continue

        rows = page.locator("#vinStandardEquipment table.vinInfoTable tbody tr")
        count = rows.count()

        vehicle = {} #current vehicle
        equipment_codes = [] #list of codes
        equipment_status = []  # list of status yes no
        equipment_descs = [] #list of descriptions

        for i in range(count):
            tds = rows.nth(i).locator("td")
            if tds.count() < 3:
                continue

            code = tds.nth(0).inner_text().strip()
            yesno = tds.nth(1).inner_text().strip()
            desc = tds.nth(2).inner_text().strip()

            if yesno.lower() != "yes":
                continue

            equipment_codes.append(code)
            equipment_descs.append(desc)

        vehicle["VIN"] = vin
        vehicle["Equipment Codes"] = "||".join(equipment_codes)
        vehicle["Equipment Description"] = "||".join(equipment_descs)

        vins_extracted += 1
        data.append(vehicle)

    df = pd.DataFrame(data)
    df.to_excel(f'fiat_100_output.xlsx', index=False)

    browser.close()

    #max 29 vins