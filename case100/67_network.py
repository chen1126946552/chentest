# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
d = DesiredCapabilities.CHROME
# d['loggingPrefs'] = {'driver': 'ALL'}
d['loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome('./chromedriver', desired_capabilities=d)
# driver = webdriver.Firefox(executable_path='./geckodriver', desired_capabilities=d)

driver.get("https://www.ptengine.com")
time.sleep(5)
for entry in driver.get_log('performance'):
    print(entry)
driver.quit()