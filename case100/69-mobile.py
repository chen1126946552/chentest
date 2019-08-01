from selenium import webdriver
from time import sleep

#设置手机型号
mobileEmulation = {'deviceName': 'iPhone 5'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)
#启动driver
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
#访问简书页
driver.get('http://www.ptengine.com')
sleep(10)    # 设置页面打开后停留时间，时间设长点可以通过滚动条看得更明显
driver.quit()

