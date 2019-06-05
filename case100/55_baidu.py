# -*- coding: UTF-8 -*-

from selenium import webdriver
import time

browser = webdriver.Chrome('/Users/chenchen/Desktop/chentest/chentest/case100/chromedriver')
browser.get('http://dashv2.datadeck.com/')

email = browser.find_element_by_name('email')
email.send_keys('chen@ptthink.com')
userPassword = browser.find_element_by_name('userPassword')
userPassword.send_keys('ptmind2008')

commit = browser.find_element_by_class_name('pt-ui-button')
commit.click()
time.sleep(3)
browser.quit()