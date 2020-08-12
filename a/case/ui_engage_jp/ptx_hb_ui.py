# -*- coding: utf-8 -*-
# UI访问页面，查看engage有正常展示，且为测试账号构造数据

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

login_url = "https://x.ptengine.jp/app/login"
hb_engage_url = "http://datatest16.ptmind.com/ptx/index.html"

def test_01(browser):

    browser.get(login_url)
    email = browser.find_element_by_xpath('//*[@id="ptx"]/div/div/div[2]/div[1]/div/div[2]/input')
    email.send_keys('chen.chen@ptmind.com')
    userPassword = browser.find_element_by_xpath('//*[@id="ptx"]/div/div/div[2]/div[2]/div/div[2]/input')
    userPassword.send_keys('123456')

    commit = browser.find_element_by_tag_name('button')
    commit.click()
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Home_body_uC320"))
        )
        home = 'True'
    except:
        home = 'False'
    assert home == 'True'

def test02_engage(browser):
        '''检查engage弹出'''
        browser.get(hb_engage_url)
        time.sleep(5)
        try:
            browser.find_element_by_id('ptxEngage')
            ptEngage = 'True'
        except:
            ptEngage = 'False'
        print('页面肯定存在，ptxEngage元素')
        assert ptEngage == 'True'

