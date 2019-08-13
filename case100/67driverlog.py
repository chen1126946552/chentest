# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome('./chromedriver', desired_capabilities=d)

driver.get("http://baidu.com")

for entry in driver.get_log('performance'):
    print(entry)
    print('----------------------')

driver.quit()
