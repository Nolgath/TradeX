import time
from playwright.sync_api import sync_playwright
import pandas as pd
from io import BytesIO

def openlane_scrape():
    status = ['notReadyForSale', 'readyForSale', 'auctionOngoing']
    # status = ['notReadyForSale']
    USERNAME = 'mh@tradex-auto.com'
    PASSWORD = 'TRADExAMS2n2025+!'

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-setuid-sandbox",
                "--single-process"
            ]
        )

        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
            java_script_enabled=True
        )
        page = context.new_page()
        page.goto('about:blank')
        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        time.sleep(3)
        page.goto('https://okta.iam.karglobal.com/app/okta_org2org/exk35eesxnP4zEMGM0i7/sso/saml')
        print("Current URL:", page.url)
        page.fill('#idp-discovery-username', USERNAME)
        page.keyboard.press('Enter')
        page.fill('#okta-signin-password', PASSWORD)
        page.keyboard.press('Enter')
        time.sleep(5)
        page.wait_for_load_state("networkidle")
        page.goto('https://sell.openlane.eu/vehicles?status=readyForSale')
        print("Current URL:", page.url)
        print('login button click phase')
        page.wait_for_selector('#login-button', state='visible', timeout=15000).click()
        # page.click('#login-button')
        page.wait_for_load_state("networkidle")
        time.sleep(5)
        car_id = []
        results = []

        for n in status:
            page.goto(f'https://sell.openlane.eu/vehicles?status={n}')
            page.wait_for_load_state("networkidle")
            #Get count of vehicles
            while True:
                rows_vd = page.locator("a._flexContainer_5p7wh_1")
                count = rows_vd.count()
                print(f"Found {count} vehicles")
                for i in range(count):
                    href = rows_vd.nth(i).get_attribute("href")
                    car_id.append(href)
                next_btn = page.locator('button:has(svg[data-icon="chevron-right"])')
                # If the button is not found → stop
                if next_btn.count() == 0:
                    break
                # If the button exists but is disabled → stop
                if next_btn.is_disabled():
                    break
                next_btn.click()
                page.wait_for_timeout(2000)
            #Extraction
            for link in car_id:
                vehicle = {}
                car = f'https://sell.openlane.eu{link}/stockManagement'
                page.goto(car)
                time.sleep(2)
                page.wait_for_load_state("networkidle")
                loc = page.locator('[data-testid="adesaEstimatedSalesPrice"]')
                price = loc.get_attribute("value") if loc.count() else 0
                loc = page.get_by_text("VIN:")
                if loc.count():
                    txt = loc.first.inner_text()
                    vin = txt.split("VIN:")[1].strip()
                else:
                    vin = ""
                results.append({"VIN": vin, "Price": price})
                print(f'{vin} | {price} | {n}')
                vehicle['VIN'] = vin
                vehicle['Price'] = price
                vehicle['Status'] = n
                results.append(vehicle)

            time.sleep(3)

        result_df = pd.DataFrame(results)

        # Write to BytesIO (in-memory file)
        output = BytesIO()
        result_df.to_excel(output, index=False)
        output.seek(0)
        browser.close()
        return output

#Get Bid and VAT and VIN
#Get History Prices for each car