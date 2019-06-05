from selenium import webdriver
brower = webdriver.Firefox()
brower.get('https://www.taobao.com')
print(brower.page_source)
brower.close()