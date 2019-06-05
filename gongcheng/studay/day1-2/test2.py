# -*- coding: UTF-8 -*-
# 8中定位元素方法
from selenium import webdriver

import time

driver = webdriver.Firefox()

driver.get('https://www.baidu.com')

# 方法一： 通过id定位，id唯一
driver.find_element_by_id('kw').send_keys('find')

time.sleep(5)

driver.find_element_by_id('kw').clear()

driver.find_element_by_id('kw').click()

# 方法二： 通过name, 可能重复
driver.find_element_by_name('tj_trnews')

# 方法三:  class属性，确定唯一性
driver.find_element_by_class_name('s_ipt').send_keys('chazhao')

# 方法四： tag 标签 , 很少用到
driver.find_element_by_tag_name('from')

# 方法五六: link
driver.find_element_by_link_text('地图')
driver.find_element_by_partial_link_text('部分') #匹配部分文本

# 方法七: xpath, 大部分使用
driver.find_element_by_xpath("//*[@id='lg']/map/area")

# 方法八: css
driver.find_element_by_css_selector()

# 复数定位
driver.find_elements_by_class_name('mnav')[0].click()



driver.quit()


