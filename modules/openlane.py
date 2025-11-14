import time

from playwright.sync_api import sync_playwright
import pandas as pd


USERNAME = 'mh@tradex-auto.com'
PASSWORD = 'TRADExAMS2n2025+!'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://sell.openlane.eu/vehicles?status=all')

    time.sleep(10)
    browser.close()
