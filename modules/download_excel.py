import requests
import os
from datetime import datetime, timedelta

today = datetime.now()
last_month = today - timedelta(days=180)
today_str = today.strftime("%d.%m.%Y")
last_month_str = last_month.strftime("%d.%m.%Y")

def download_excel_stock():
    # delete old file if exists
    if os.path.exists("../stock_list.xlsx"):
        os.remove("../stock_list.xlsx")

    session = requests.Session()
    payload = {
        'username': 'c.zorila',
        'password': 'MemoCristian2025'
    }

    session.post('https://ams-de.mega-moves.com/', data=payload)
    r = session.get('https://ams-de.mega-moves.com/portal/after-sale/pages/list-export-inventory.php?action=bestandsliste')

    with open("../stock_list.xlsx", "wb") as f:
        f.write(r.content)

def download_excel_sales():
    if os.path.exists("../sales_list.xlsx"):
        os.remove("../sales_list.xlsx")

    LOGIN_URL = "https://ams-de.mega-moves.com/"
    DOWNLOAD_URL = "https://ams-de.mega-moves.com/portal/after-sale/pages/list-export-sales.php"

    USERNAME = "c.zorila"
    PASSWORD = "MemoCristian2025"

    session = requests.Session()
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    login_response = session.post(LOGIN_URL, data=payload)
    login_response.raise_for_status()

    # The form data you saw in the HTML
    form_data = {
        "verkaufsliste_von": last_month_str,
        "verkaufsliste_bis": today_str
    }

    # Post to the form's action URL
    response = session.post(DOWNLOAD_URL, data=form_data)

    # Save the resulting file
    with open("../sales_list.xlsx", "wb") as f:
        f.write(response.content)

download_excel_sales()
download_excel_stock()