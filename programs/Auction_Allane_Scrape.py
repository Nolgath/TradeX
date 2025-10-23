import time
import pandas as pd
from playwright.sync_api import sync_playwright

results = []

def auction_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://auth.haendlerboerse.de/login?style=allane&lang=en&platformUrl=https://www.haendlerboerse.de")
        #Login
        page.fill("input[name=username]", "purchase@tradex-auto.com")
        page.fill("input[name=password]", "AMSPurchase2025!")
        page.click("button[type=submit]")
    #---------------------------------------START
        page.goto('https://www.haendlerboerse.de/buy/online/car/list')

        time.sleep(3)
        n_of_cars = page.locator('.AllVehiclesListCounter').inner_text()
        page.locator("div[id^='article_id_']").first.click()

        for i in range(int(n_of_cars)):
            page.wait_for_selector("#identification_nr .col-xs-7.col-sm-6", timeout=10000)

            def safe_text(page, selector):
                if page.locator(selector).count() == 0:
                    return "N/A"
                page.wait_for_selector(selector, timeout=5000)
                return page.locator(selector).first.inner_text()

            starting_price = safe_text(page, "span#start_amount")
            price = starting_price.replace("Startpreis:", "").replace("€", "").replace('.', ',').strip()
            vin = safe_text(page, "#identification_nr .col-xs-7.col-sm-6")
            brand = safe_text(page, "#brand .col-xs-7.col-sm-6")
            model = safe_text(page, "#model .col-xs-7.col-sm-6")
            bodytype = safe_text(page, "#construction .col-xs-7.col-sm-6")
            type = safe_text(page, "#type .col-xs-7.col-sm-6")
            doors = safe_text(page, "#doors .col-xs-7.col-sm-6")
            construction_year = safe_text(page, "#construction_year .col-xs-7.col-sm-6")
            reg_date = safe_text(page, "#registration_date .col-xs-7.col-sm-6")
            mileage = safe_text(page, "#mileage .col-xs-7.col-sm-6")
            co2_emission = safe_text(page, "#co2_emission .col-xs-7.col-sm-6")
            registration_number = safe_text(page, "#registration_number .col-xs-7.col-sm-6")
            cubic_capacity = safe_text(page, "#cubic_capacity .col-xs-7.col-sm-6")
            motor_type = safe_text(page, "#motor_type .col-xs-7.col-sm-6")
            power = safe_text(page, "#power .col-xs-7.col-sm-6")
            color_exact = safe_text(page, "#color_exact .col-xs-7.col-sm-6")
            transmission = safe_text(page, "#transmission .col-xs-7.col-sm-6")

            results.append({
                'Vin': vin, 'Start Price': price, 'Brand': brand, 'Model': model,
                'Bodytype': bodytype, 'Type': type, 'Doors': doors, 'Construction Year': construction_year,
                'Registration Date': reg_date, 'Mileage': mileage, 'CO2 Emission': co2_emission,
                'Registration Number': registration_number, 'Cubic Capacity': cubic_capacity,
                'Motor Type': motor_type, 'Power': power, 'Color Exact': color_exact, 'Transmission': transmission
            })

            if page.get_by_text("nächstes Angebot").count() == 0:
                break

            page.get_by_text("nächstes Angebot").click()
            page.wait_for_load_state("domcontentloaded")

        browser.close()

    df = pd.DataFrame(results)
    df.to_excel("auction_allane.xlsx",index=False)