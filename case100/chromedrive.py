
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.common.service

# browser = webdriver.Chrome('./chromedriver')
# browser.get('http://dashv2.datadeck.com/')

# email = browser.find_element_by_name('email')
# email.send_keys('chen@ptthink.com')
# userPassword = browser.find_element_by_name('userPassword')
# userPassword.send_keys('ptmind2008')
#
# commit = browser.find_element_by_class_name('pt-ui-button')
# commit.click()
# time.sleep(3)



capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}

driver = webdriver.Chrome('./chromedriver',desired_capabilities=capabilities)

driver.get('www.ptengine.com')

# print console log messages
for entry in driver.get_log('browser'):
    print(entry)

driver.quit()