# -*- coding: UTF-8 -*-
# 登录

from selenium import webdriver
import time

def logins(driver):
    driver.get('http://staging.datadeck.com')
    time.sleep(5)
    driver.find_element_by_name('email').send_keys('chen.chen@ptmind.com')
    driver.find_element_by_name('userPassword').send_keys('123456789')
    driver.find_element_by_tag_name('button').click()
    time.sleep(10)

# 前提在DD Dashboard List页面
def add_dashboard(driver):
    driver.find_element_by_class_name('add-node-tools-pos').click()
    driver.find_elements_by_class_name('pt-select__dropdown-item')[0].click()
    time.sleep(10)

# 在一个面板页面
def add_widget(driver):
    driver.find_element_by_class_name('pt-ui-button__text').click()
    driver.find_element_by_css_selector('.dashboard__header-more>ul>li').click()
    time.sleep(5)

if (__name__ == "__main__"):
    driver = webdriver.Firefox()
    logins(driver)
    add_dashboard(driver)
    add_widget(driver)
    driver.quit()