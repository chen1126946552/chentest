
from selenium import webdriver
import time

browser = webdriver.Chrome('./chromedriver')
# browser.get('http://dashv2.datadeck.com/')

# email = browser.find_element_by_name('email')
# email.send_keys('chen@ptthink.com')
# userPassword = browser.find_element_by_name('userPassword')
# userPassword.send_keys('ptmind2008')
#
# commit = browser.find_element_by_class_name('pt-ui-button')
# commit.click()
# time.sleep(3)

browser.get('http://datatest11.ptmind.com/cnonline_auto/checklist.html')
time.sleep(5)
try:
    browser.find_element_by_id('ptEngage')
    a = 'True'
except:
    a = 'False'
print(a)



browser.quit()