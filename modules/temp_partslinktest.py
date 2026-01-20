from playwright.sync_api import sync_playwright,TimeoutError
import time
import pandas as pd

df = pd.read_excel('vins.xlsx')

audi = 'https://www.partslink24.com/p5/latest/p5.html#%2Fp5vwag~audi_parts~en~'
vw = 'https://www.partslink24.com/p5/latest/p5.html#%2Fp5vwag~vw_parts~en~'
vins = df['VIN'].tolist()
brands = df['brand'].str.lower().tolist()
brands_url = {'audi': audi, 'vw': vw, }
print(vins)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    username = "Admin-PT"
    password = "trAdEx2025*!"
    id = "de-800610"
    page.goto("https://www.partslink24.com/")
    page.fill("#login-name", username)
    page.fill("#inputPassword", password)
    page.fill('#login-id', id)
    page.keyboard.press("Enter")

    print('Searching for "Confirm"')
    try:
        page.wait_for_selector('#squeezeout-login-btn', timeout=2000)
        page.click('#squeezeout-login-btn')
    except TimeoutError:
        pass

    data = []

    for vin, brand in zip(vins, brands):
        print(f'Extracting : {vin}')
        if brand in brands_url:
            url = brands_url[brand] + vin
        time.sleep(1)
        page.goto(url)
        page.wait_for_load_state("networkidle")
        # vehicle data
        page.wait_for_selector("[id^='vinfoBasic_c']")
        rows = page.locator("[id^='vinfoBasic_c']").all()
        vehicle = {}
        for row in rows:
            desc = row.locator(".p5_table_cell_comp.p5t14_description").inner_text()
            value = row.locator(".p5_table_cell_comp.p5t14_value").inner_text()
            vehicle[desc] = value
        data.append(vehicle)
        page.locator(".p5_accordion_header").nth(1).click()
        rows_vd = page.locator("[id^='prNr_c']")
        count = rows_vd.count()
        equipment_codes = []
        equipment_descs = []

        dont_include = ['without','possible','on demand']

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
            attribute = attr_text
            equipment_code = code_text
            equipment_desc = desc_text

            equipment_codes.append(equipment_code)
            equipment_descs.append(equipment_desc)


        clean_codes = [x.replace("\n", " ").strip() for x in equipment_codes]
        clean_desc = [x.replace("\n", " ").strip() for x in equipment_descs]
        vehicle["Equipment Codes"] = "|".join(clean_codes)
        vehicle["Equipment Descriptions"] = "|".join(clean_desc)
        time.sleep(3)
    browser.close()

df_output = pd.DataFrame(data)
df_output.to_excel("partslink_output.xlsx", index=False)