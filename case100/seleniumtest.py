# -*- coding: utf-8 -*-

from selenium import webdriver
import time

if __name__ == "__main__":
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_argument("--headless")
    chrome_opt.add_argument('--no-sandbox')
    chrome_opt.add_argument('--disable-gpu')
    chrome_opt.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/Users/chenchen/Desktop/pt-gitlab/chromedriver', chrome_options=chrome_opt)

    driver.get('http://datatest12.ptmind.com/chen/test3.html')
    time.sleep(10)
    try:
        driver.find_element_by_id('ptEngage')
        ptEngage = 'True'
    except:
        ptEngage = 'False'
    print(ptEngage)
    driver.quit()


