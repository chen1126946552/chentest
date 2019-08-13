# -*- coding: utf-8 -*-
from selenium import webdriver
import time

options = webdriver.ChromeOptions()

# 谷歌无头模式
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug

# options.add_argument('disable-infobars')  # 隐藏"Chrome正在受到自动软件的控制"
# options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
# options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
# options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# options.add_argument('--remote-debugging-port=9222')
# options.binary_location = r'/Applications/Chrome'  # 手动指定使用的浏览器位置

# 更换头部
# user_agent = (
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
#         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
# )
# options.add_argument('user-agent=%s' % user_agent)

# 设置图片不加载
# prefs = {
#     'profile.default_content_setting_values': {
#         'images': 2
#     }
# }
# options.add_experimental_option('prefs', prefs)
# # 或者  使用下面的设置, 提升速度
# options.add_argument('blink-settings=imagesEnabled=false')

# # 设置代理
# options.add_argument('proxy-server=' + '192.168.0.28:808')

driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get('www.ptengine.com')
time.sleep(20)
driver.quit()
# # 设置cookie
# driver.delete_all_cookies()  # 删除所有的cookie
# driver.add_cookie({'name': 'ABC', 'value': 'DEF'})  # 携带cookie打开
# driver.get_cookies()
#
# # 通过js新打开一个窗口
# driver.execute_script('window.open("https://www.baidu.com");')