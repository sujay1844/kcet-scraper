#!/usr/bin/env python

# A web scraper to check for updates in KCET-2022 website announcements section
# I can't check every 10 minutes for the link to enter college course options
# The KEA was supposed to post the link to the portal at 2022-10-14 01:00PM
# Right now it is 2022-10-14 05:00PM

# If you want to automate this script, then manually set the browser_choice

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("""
Supported browsers:
1 Chrome
2 Firefox
3 Chromium
4 Microsoft Edge
""")
browser_choice = input("Enter your choice: ")

# Download the required driver automatically
if browser_choice.lower() == "1":
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

elif browser_choice.lower() == "2":
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.options import Options
    firefox_options = Options()
    # Disable image loading for better performance
    firefox_options.set_preference('permissions.default.image', 2)
    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

elif browser_choice.lower() == "3":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromiumService
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.utils import ChromeType

    browser = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    
elif browser_choice.lower() == "4":
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

else:
    print("Choose a number from 1 to 4")
    exit(1)

# Open up the URL
URL = "https://cetonline.karnataka.gov.in/kea/"
browser.get(URL)

# Change language to english
time.sleep(0.1)
try:
    browser.find_element(By.XPATH, "/html/body/nav/button").click()
except Exception as e:
    print()

time.sleep(0.1)
browser.find_element(By.XPATH, '/html/body/nav/div/form/div[3]/select/option[2]').click()
time.sleep(0.1)

# Parse entries into an array
entries = []
for i in range(100):
    table_entry = browser.find_elements(By.XPATH, f'//*[@id="ContentPlaceHolder1_Gridlatestannoc_hypertext_{i}"]')
    try:
        entries.insert(0, table_entry[0].text)
    except IndexError:
        break

browser.close()
print("\nEntries:\n")
print(*entries, sep="\n")
