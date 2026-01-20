from playwright.sync_api import sync_playwright
import time
import pandas as pd

df = pd.read_excel('vins.xlsx')

vins = df['VIN'].tolist()
regs = df['First Reg'].tolist()
mileages = [int(round(x)) for x in df['Mileage']]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://de.schwacke.de/auth/login")

    page.wait_for_selector("#ccc-recommended-settings")
    page.click("#ccc-recommended-settings")

    # login
    page.fill('input[placeholder="Mailadresse eingeben"]', "marcel.hein@auto-mega-store.com")
    page.fill('input[placeholder="Passwort eingeben"]', "0RxHIW2n2026+!")
    page.click('button[type="submit"]')

    page.wait_for_selector('button:has-text("Ja")')
    page.click('button:has-text("Ja")')

    results = []

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

        page.wait_for_load_state("networkidle",timeout=60000)
        time.sleep(1)

        rows = page.query_selector_all('div.ag-center-cols-container .ag-row')
        if len(rows) == 1:
            page.locator('div[role="row"][row-id="0"]').click()
            # page.locator("vpfa-arrow-link:has-text('Technische Daten')").click()
            page.locator("vpfa-arrow-link:has-text('Fahrzeugdetails')").click()
            page.wait_for_selector("form")

            fields = page.locator("vpfa-setting-box")

            data = {}
            for i in range(fields.count()):
                f = fields.nth(i)
                label = f.locator("span.label-text").first.inner_text().strip()
                # Try input
                if f.locator("input.ant-input").count() > 0:
                    value = f.locator("input.ant-input").first.input_value().strip()
                # Try select
                elif f.locator("nz-select-item").count() > 0:
                    value = f.locator("nz-select-item").first.inner_text().strip()
                elif f.locator("nz-select-placeholder").count() > 0:
                    value = f.locator("nz-select-placeholder").first.inner_text().strip()
                else:
                    value = ""
                data[label] = value

            color = data.get("ORIGINAL-HERSTELLERFARBE", "")
            #----------------------------------------------------------------------------------------------

            page.locator("vpfa-setting-box:has-text('MwSt.-Art') nz-select").click()
            time.sleep(1)
            page.keyboard.press("Enter")
            time.sleep(0.5)
            # blur nz-select to close dropdown
            page.evaluate("document.activeElement.blur()")
            time.sleep(0.5)
            page.keyboard.press("End")
            time.sleep(1)
            page.get_by_role("button", name="Speichern").click()

            # ----------------------------------------------------------------------------------------------
            page.locator("button:has-text(' Mehr anzeigen ')").click()
            price = page.locator("#avRetailPrice").inner_text()
            print(vin,':',price,'|',color)
            pass
        elif "https://de.schwacke.de/valuations/" in page.url:
            page.locator('div[role="row"][row-id="0"]').click()
            # page.locator("vpfa-arrow-link:has-text('Technische Daten')").click()
            page.locator("vpfa-arrow-link:has-text('Fahrzeugdetails')").click()
            page.wait_for_selector("form")
            fields = page.locator("vpfa-setting-box")
            data = {}
            for i in range(fields.count()):
                f = fields.nth(i)
                label = f.locator("span.label-text").first.inner_text().strip()
                # Try input
                if f.locator("input.ant-input").count() > 0:
                    value = f.locator("input.ant-input").first.input_value().strip()
                # Try select
                elif f.locator("nz-select-item").count() > 0:
                    value = f.locator("nz-select-item").first.inner_text().strip()
                elif f.locator("nz-select-placeholder").count() > 0:
                    value = f.locator("nz-select-placeholder").first.inner_text().strip()
                else:
                    value = ""
                data[label] = value

            color = data.get("ORIGINAL-HERSTELLERFARBE", "")

            page.locator("vpfa-setting-box:has-text('MwSt.-Art') nz-select").click()
            time.sleep(1)
            page.keyboard.press("Enter")
            time.sleep(0.5)
            # blur nz-select to close dropdown
            page.evaluate("document.activeElement.blur()")
            time.sleep(0.5)
            page.keyboard.press("End")
            time.sleep(1)
            page.get_by_role("button", name="Speichern").click()
#
            page.locator("button:has-text(' Mehr anzeigen ')").click()
            price = page.locator("#avRetailPrice").inner_text()
            print(vin,':',price,'|',color)
            pass
        current_url = page.url
        time.sleep(1)
        page.goto(f'{current_url}/equipment')
        page.wait_for_load_state("networkidle",timeout=60000)

        dropdown = page.locator('.ag-floating-filter-full-body nz-select')
        dropdown.click()
        page.wait_for_selector('.cdk-overlay-container nz-option-item[title="ausgewählt"]')
        page.locator('.cdk-overlay-container nz-option-item[title="ausgewählt"]').click()
        page.click('body')

        # Packages
        page.locator('#package-section').click()
        rows = page.locator('.ag-center-cols-container [role="row"]')
        for i in range(rows.count()):
            item = rows.nth(i).locator('[col-id="Item"]').inner_text().strip()
            results.append({"VIN": vin, "Type": "Package", "Equipment": item})

        # Optional
        page.locator('#optional-section').click()
        rows = page.locator('.ag-center-cols-container [role="row"]')
        for i in range(rows.count()):
            item = rows.nth(i).locator('[col-id="Item"]').inner_text().strip()
            results.append({"VIN": vin, "Type": "Optional", "Equipment": item})

        # Standard
        page.locator('#standard-section').click()
        rows = page.locator('.ag-center-cols-container [role="row"]')
        for i in range(rows.count()):
            item = rows.nth(i).locator('[col-id="Item"]').inner_text().strip()
            results.append({"VIN": vin, "Type": "Standard", "Equipment": item})


        print(results)
        page.goto('https://de.schwacke.de/')

    df_out = pd.DataFrame(results)
    df_out.to_excel("equipment_results.xlsx", index=False)

    time.sleep(5)
    browser.close()