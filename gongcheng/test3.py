# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains

import time
from selenium.webdriver.support.select import Select



driver = webdriver.Firefox()

driver.get('https://www.baidu.com')

time.sleep(5)

mouse = driver.find_element_by_link_text('设置')

ActionChains(driver).move_to_element(mouse).perform() # 鼠标悬停
time.sleep(5)

# 定位到select元素对象
select_element = driver.find_element_by_link_text('')
# 用select方法定位
Select(select_element).select_by_index(1)
# 如果下拉框没有收回
select_element.click()

al = driver.switch_to_alert # 旧语法
al = driver.switch_to.alert # 新语法
al.accept()
al.dismiss()
al.send_keys()

# 执行js
js = '$(".prefpanelgo").click()'
driver.execute_script(js)

driver.quit()