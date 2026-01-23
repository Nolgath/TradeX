from playwright.sync_api import sync_playwright,TimeoutError
import time
import pandas as pd
from io import BytesIO

def partslink(df,country):
    open("logs.txt", "w").close()  # clears file
    with open("logs.txt", "a") as f:
        f.write("Extraction starting...")
        f.flush()

    vw = 'https://www.partslink24.com/p5/latest/p5.html#%2Fp5vwag~vw_parts~en~'
    vins = df['VIN'].tolist()
    brands = df['brand'].str.lower().tolist()
    brands_url = {'vw': vw}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        id = "de-800610"

        if country == 'Portugal':
            username = "Admin-PT"
            password = "trAdEx2025*!"
        else:
            username = "admin"
            password = "AmS2024!"

        page.goto("https://www.partslink24.com/")
        if page.locator("[data-testid='uc-accept-all-button']").count():
            page.locator("[data-testid='uc-accept-all-button']").click()

        page.fill("#login-name", username)
        page.fill("#inputPassword", password)
        page.fill('#login-id', id)
        page.keyboard.press("Enter")

        time.sleep(3)

        if page.locator("[data-testid='uc-accept-all-button']").count():
            page.locator("[data-testid='uc-accept-all-button']").click()

        time.sleep(3)

        page.locator("#squeezeout-login-btn").wait_for(timeout=15000)
        page.locator("#squeezeout-login-btn").click()

        time.sleep(3)

        data = []

        for vin,brand in zip(vins,brands):
           if brand in brands_url:
               print(f'Trying : {vin} | brand : {brand}')
               if brand.lower() in brands_url:
                   url = brands_url[brand] + vin
               print(f'Navigating to : {url}')
               page.goto(url)
               time.sleep(2)

               #vehicle data
               try:
                   page.wait_for_selector("[id^='vinfoBasic_c']", timeout=30000)
                   print(f'Working on {brand} | {vin}')
                   open("logs.txt", "w").close()  # clears file
                   with open("logs.txt", "a") as f:
                       f.write(f'Working on : {brand} | {vin}')
                       f.flush()


               except TimeoutError:
                   print(f"Skipping {vin} – selector not found")
                   open("logs.txt", "w").close()  # clears file
                   with open("logs.txt", "a") as f:
                       f.write(f'Not found : {brand} | {vin}')
                       f.flush()

                   time.sleep(2)
                   page.goto('https://www.partslink24.com/partslink24/startup.do')
                   continue  # go to next VIN

               rows = page.locator("[id^='vinfoBasic_c']").all()
               vehicle = {}
               for row in rows:
                   desc = row.locator(".p5_table_cell_comp.p5t14_description").inner_text()
                   value = row.locator(".p5_table_cell_comp.p5t14_value").inner_text()
                   vehicle[desc] = value
               data.append(vehicle)
               print(f'Opening Equipment Accordion (continuing...)')
               page.locator(".p5_accordion_header").nth(1).click()
               rows_vd = page.locator("[id^='prNr_c']")
               count = rows_vd.count()
               equipment_full_all = []
               dont_include = ['without', 'possible', 'on demand']

               for i in range(count):
                   attr_text = rows_vd.nth(i).locator("div.p5_table_cell_comp.p5t15_col1").inner_text()
                   code_text = rows_vd.nth(i).locator("div.p5_table_cell_comp.p5t15_col2").inner_text()
                   desc_text = rows_vd.nth(i).locator("div.p5_table_cell_comp.p5t15_col3").inner_text()
                   # skip if any forbidden word appears
                   if any(word in attr_text.lower() for word in dont_include):
                       continue
                   if any(word in code_text.lower() for word in dont_include):
                       continue
                   if any(word in desc_text.lower() for word in dont_include):
                       continue
                   # valid → append values
                   equipment_full = code_text+f'({desc_text})'

                   equipment_full_all.append(equipment_full)

               clean_all = [x.replace("\n", " ").strip() for x in equipment_full_all]
               vehicle["Equipments"] = "|".join(clean_all)
               page.goto('https://www.partslink24.com/partslink24/startup.do')
               print(f'Extracted : {vin}')
           else:
               print(f'Bad brand : {vin}')
               continue
        time.sleep(5)
        open("logs.txt", "w").close()  # clears file
        with open("logs.txt", "a") as f:
            f.write(f"Complete")
            f.flush()
        browser.close()

    df_output = pd.DataFrame(data)
    output = BytesIO()
    df_output.to_excel(output, index=False)
    output.seek(0)
    time.sleep(2)
    open("logs.txt", "w").close()  # clears file
    return output
