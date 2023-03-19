import sqlite3
from selenium import webdriver
import requests
import os

SCREENSHOTS_DIR = "/var/lib/screenshot"


def make_screenshot(proto):
    browser.get(f'{proto}://{row[1]}')
    r = requests.get(f'{proto}://{row[1]}', verify=False)
    if not os.path.exists(f'{SCREENSHOTS_DIR}/{r.status_code}'):
        os.makedirs(f'{SCREENSHOTS_DIR}/{r.status_code}')
    port = 80 if proto == "http" else 443
    browser.save_screenshot(f'{SCREENSHOTS_DIR}/{r.status_code}/{row[1]}_{port}.png')


options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
browser = webdriver.Chrome(options=options)

sqlite_connection = sqlite3.connect('domains.db')
cursor = sqlite_connection.cursor()

cursor.execute("select * from domains where http is 1 or https is 1")
rows = cursor.fetchall()
for row in rows:
    print(f'working on {row[1]}')
    try:
        if row[2]:
            make_screenshot("http")
    except Exception as ex:
        print(ex.message)
        pass
    try:
        if row[3]:
            make_screenshot("https")
    except Exception as ex:
        print(ex.message)
        pass
