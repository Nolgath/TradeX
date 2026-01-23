import time
from playwright.sync_api import sync_playwright
from modules.transport_data import car_ids
from modules.logs_config import LOGS_FILE
import pandas as pd

def transport_price_input(df,user,password):
    open(LOGS_FILE, "w", encoding='utf-8').close()  # clears file
    with open(LOGS_FILE, "a", encoding='utf-8') as f:
        f.write("Extraction starting...")
        f.flush()
    PROVIDER_PAGE = 'https://ams-de.mega-moves.com/portal/vehicles/pages/vehicle-details-4.php?wgID='
    INT_REMARK_PAGE = 'https://ams-de.mega-moves.com/portal/vehicles/pages/vehicle-details-5.php?wgID='
    MAIN_PAGE = 'https://ams-de.mega-moves.com/portal/vehicles/pages/vehicle-details.php?wgID='

    excel = df.to_dict(orient='records')

    logs = []

    #login
    username = user
    password = password

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
    #Login into the page.
        page.goto("https://ams-de.mega-moves.com/")
        page.fill("input[name=username]", username)
        page.fill("input[name=password]", password)
        page.click("button[type=submit]")

        for i in excel:
            number_of_cars = len(excel)
            vin = i['vin']
            car_id = car_ids(vin)
            load = i['load']
            count_same_load = sum(1 for d in excel if d['load'] == load)
            price = i['load_price']
            transport_name = i['transport_name']
            delivery_country = i['delivery_country']
            location = i['location']
            output_date = i['output_date']
            t_type = int(i['type'])
            calculate_p_car = str(round(price / count_same_load, 2))
            full_transport_label = f'Transport {transport_name} {delivery_country}'

            print('#-------------------------NEXT:------------------------')
            print(f'Processing {vin}...')
            open(LOGS_FILE, "w", encoding='utf-8').close()
            with open(LOGS_FILE, "a", encoding='utf-8') as f:
               f.write(f'Processing {vin}...')
               f.flush()
            print('#------------------------------------------------------')
        #------------------------------------------------------------------------------------------------------
            if pd.notna(location) and str(location).strip():
                to_provider = PROVIDER_PAGE+car_id
                time.sleep(3.5)
                page.goto(to_provider)
                location_field = page.locator("input[name='Standort']")
                location_field.wait_for(state="visible")
                location_field.fill(str(location))
                page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')") #Save Button
                location_log = 'Location: ' + str(location)
                open(LOGS_FILE, "w", encoding='utf-8').close()
                with open(LOGS_FILE, "a", encoding='utf-8') as f:
                    f.write(f'Location added: {str(location)}')
                    f.flush()
            else:
                print(f'No location provided for {vin}')
                open(LOGS_FILE, "w", encoding='utf-8').close()
                with open(LOGS_FILE, "a", encoding='utf-8') as f:
                    f.write(f'No location provided for {vin}')
                    f.flush()
                location_log = 'Location ❌'
        #-----------------------------------------------------------------------------------------------------
            #Output Date Input:
            if pd.notna(output_date) and str(output_date).strip() != "0":
                to_int_remark = INT_REMARK_PAGE + car_id
                time.sleep(4)
                page.goto(to_int_remark, wait_until="domcontentloaded", timeout=10000)
                formatted_date = pd.to_datetime(output_date, dayfirst=True).strftime("%d.%m.%Y")
                page.eval_on_selector("#Ausgang", "el => el.removeAttribute('readonly')")
                page.locator("#Ausgang").fill(formatted_date, force=True)
                # click submit immediately
                page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')")  # Save Button
                print(f"Added output date: {formatted_date} to {vin}")
                outputdate_log = 'Output Date ✓: ' + str(output_date)

                open(LOGS_FILE, "w", encoding='utf-8').close()
                with open(LOGS_FILE, "a", encoding='utf-8') as f:
                    f.write(f"Added output date: {formatted_date} to {vin}")
                    f.flush()
            else:
                print(f"No output date provided for {vin}")
                outputdate_log = 'Output Date ❌'
                open(LOGS_FILE, "w", encoding='utf-8').close()
                with open(LOGS_FILE, "a", encoding='utf-8') as f:
                    f.write(f"No output date provided for {vin}")
                    f.flush()

            #-----------------------------------------------------------------------------------------------------
            if t_type != 0:
                to_int_remark = INT_REMARK_PAGE + car_ids(vin)
                time.sleep(3)
                page.goto(to_int_remark)
                time.sleep(2)

                # -----------------------------------------------------------------------INTERNAL COST
                page.wait_for_selector('[id^="v_user_input_label_"]')
                get_v = page.locator('[id^="v_user_input_label_"]').all()
                v_list = []
                v_values = []
                for el in get_v:
                    el_id = el.get_attribute("id")
                    if not el_id or not el_id.split("_")[-1].isdigit():
                        continue
                    v_list.append(el_id)
                    val = page.get_attribute(f"#{el_id}", "value") or ""
                    v_values.append(val)
                v_label = v_list[-1] #last id empty
                v_value = v_label.replace('label', 'value')
                values_v = v_values
                # -----------------------------------------------------------------------EXTERNAL COST
                page.wait_for_selector('[id^="e_user_input_label_"]')
                get_e = page.locator('[id^="e_user_input_label_"]').all()
                e_list = []
                e_values = []
                for el in get_e:
                    el_id = el.get_attribute("id")
                    if not el_id or not el_id.split("_")[-1].isdigit():
                        continue
                    e_list.append(el_id)
                    val = page.get_attribute(f"#{el_id}", "value") or ""
                    e_values.append(val)
                e_label = e_list[-1]  # last id empty
                e_value = e_label.replace('label', 'value')
                values_e = e_values
                # -----------------------------------------------------------------------INTERNAL TRANSPORT COST
                page.wait_for_selector('[id^="it_user_input_label_"]')
                get_it = page.locator('[id^="it_user_input_label_"]').all()
                it_list = []
                it_values = []
                for el in get_it:
                    el_id = el.get_attribute("id")
                    if not el_id or not el_id.split("_")[-1].isdigit():
                        continue
                    it_list.append(el_id)
                    val = page.get_attribute(f"#{el_id}", "value") or ""
                    it_values.append(val)
                it_label = it_list[-1]  # last id empty
                it_value = it_label.replace('label', 'value')
                values_it = it_values
                # -----------------------------------------------------------------------EXTERNAL TRANSPORT COST
                page.wait_for_selector('[id^="et_user_input_label_"]')
                get_et = page.locator('[id^="et_user_input_label_"]').all()
                et_list = []
                et_values = []
                for el in get_et:
                    el_id = el.get_attribute("id")
                    if not el_id or not el_id.split("_")[-1].isdigit():
                        continue
                    et_list.append(el_id)
                    val = page.get_attribute(f"#{el_id}", "value") or ""
                    et_values.append(val)
                et_label = et_list[-1]  # last id empty
                et_value = et_label.replace('label', 'value')
                values_et = et_values

                #Internal Input
                if t_type == 1:
                    print(v_values)
                    if full_transport_label in values_v:
                        print(f'Already Exists {full_transport_label}')

                        open(LOGS_FILE, "w", encoding='utf-8').close()
                        with open(LOGS_FILE, "a", encoding='utf-8') as f:
                            f.write(f'Already Exists {full_transport_label}')
                            f.flush()

                        price_input = f'Duplicate Found! Skipped.'
                        continue
                    else:
                        page.locator(f"#{v_label}").fill(f'Transport {transport_name} {delivery_country}') #Label Input
                        page.locator(f"#{v_value}").fill(calculate_p_car) #Value Input
                        page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')")  # Save Button
                        price_input = f'{calculate_p_car} on Internal Costs'
                #External Input
                if t_type == 2:
                    print(e_values)
                    if full_transport_label in values_v:
                        print(f'Already Exists {full_transport_label}')

                        open(LOGS_FILE, "w", encoding='utf-8').close()
                        with open(LOGS_FILE, "a", encoding='utf-8') as f:
                            f.write(f'Already Exists {full_transport_label}')
                            f.flush()

                        price_input = f'Duplicate Found! Skipped.'
                        continue
                    else:
                        page.locator(f"#{e_label}").fill(f'Transport {transport_name} {delivery_country}') #Label Input
                        page.locator(f"#{e_value}").fill(calculate_p_car) #Value Input
                        page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')")  # Save Button
                        price_input = f'{calculate_p_car} on External Costs'
                #Internal Transport Input
                if t_type == 3:
                    print(it_values)
                    if full_transport_label in values_v:
                        print(f'Already Exists {full_transport_label}')

                        open(LOGS_FILE, "w", encoding='utf-8').close()
                        with open(LOGS_FILE, "a", encoding='utf-8') as f:
                            f.write(f'Already Exists {full_transport_label}')
                            f.flush()

                        price_input = f'Duplicate Found! Skipped.'
                        continue
                    else:
                        page.locator(f"#{it_label}").fill(f'Transport {transport_name} {delivery_country}') #Label Input
                        page.locator(f"#{it_value}").fill(calculate_p_car) #Value Input
                        page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')")  # Save Button
                        price_input = f'{calculate_p_car} on Internal Transport Costs'
                #External Transport Input
                if t_type == 4:
                    print(et_values)
                    if full_transport_label in values_v:
                        print(f'Already Exists {full_transport_label}')

                        open(LOGS_FILE, "w", encoding='utf-8').close()
                        with open(LOGS_FILE, "a", encoding='utf-8') as f:
                            f.write(f'Already Exists {full_transport_label}')
                            f.flush()

                        price_input = f'Duplicate Found! Skipped.'
                        continue
                    else:
                        page.locator(f"#{et_label}").fill(f'Transport {transport_name} {delivery_country}') #Label Input
                        page.locator(f"#{et_value}").fill(calculate_p_car) #Value Input
                        page.evaluate("submit('/portal/vehicles/pages/vehicle-details-5.php')")  # Save Button
                        price_input = f'{calculate_p_car} on External Transport Costs'
                    time.sleep(2)
            else:
                print('No transport type selected')
                print(f'Skipping {vin} pricing inputs.')

                open(LOGS_FILE, "w", encoding='utf-8').close()
                with open(LOGS_FILE, "a", encoding='utf-8') as f:
                    f.write(f'Skipping {vin} pricing inputs. : No transport type selected')
                    f.flush()

                price_input = 'No Price Added ❌'
                continue

            open(LOGS_FILE, "w", encoding='utf-8').close()
            with open(LOGS_FILE, "a", encoding='utf-8') as f:
                f.write(f'Car: {vin} | {location_log} | {outputdate_log} | {price_input} | {MAIN_PAGE+car_id} ')
                f.flush()

        print('Done!')
        browser.close()
    return logs