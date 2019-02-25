# -*- coding: UTF-8 -*-

from selenium import webdriver
import time

driver = webdriver.Firefox()

driver.get('https://mail.163.com')
time.sleep(5)

driver.switch_to.frame(2)

driver.find_element_by_name('email').send_keys('test')
driver.find_element_by_name('password').send_keys('123456')
driver.find_element_by_id('dologin').click()
time.sleep(5)

driver.quit()