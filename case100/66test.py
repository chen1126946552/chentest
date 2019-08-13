from selenium import webdriver


chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument("--headless")
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--disable-gpu')
chrome_opt.add_argument('--disable-dev-shm-usage')
# chromedrive = "/usr/chromedriver"
chromedrive = './chromedriver'
driver = webdriver.Chrome(chromedrive, chrome_options=chrome_opt)

driver.get('https://reportv3.ptengine.jp')
commit = driver.find_element_by_tag_name('button')
commit.click()
# driver.get('http://datatest12.ptmind.com/cntest_chen/index3.html')
print(driver.get_log('browser'))
print('-------')
print(driver.get_log('driver'))
# print('-------')
# print(driver.get_log('client'))
print('-------')
# print(driver.get_log('server'))

print(driver.get_log('performance'))
