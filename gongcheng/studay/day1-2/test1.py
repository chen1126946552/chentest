from selenium import webdriver
import time

# open Firefox
driver = webdriver.Firefox()

# driver = webdriver.Chrome('/Users/chenchen/Desktop/chentest/chentest/case100/chromedriver')

driver.get('http://dashv2.datadeck.com/')
time.sleep(5)

driver.back() #左箭头
time.sleep(5)
driver.forward() #右箭头
time.sleep(5)
driver.refresh() #刷新


driver.quit()
