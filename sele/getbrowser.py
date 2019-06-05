import os
from selenium import webdriver #从selenium组件包中引入webdriver


def Chrome():
    if 'nt' in os.name:
        CDriver =os.path.join(os.path.abspath('..'),'Drivers','chromedriver.exe')

#利用相对路径去寻找Drivers文件夹的Chrome驱动文件夹（推荐）
# CDriver2 = "D:\John's CodeProject\Python-selenium\Drivers\chromedriver.exe"
#利用绝对路径去寻找Drivers文件夹的Chrome驱动文件夹

    elif 'posix' in os.name: #Mac OS X系统
        CDriver =os.path.join(os.path.abspath('..'),'Drivers','chromedriver')
        #CDriver2 = "D:\John's Code Project\Python-selenium\Drivers\chromedriver"

    os.environ['webdriver.chrome.driver'] =CDriver
    #os.environ['webdriver.chrome.driver']= CDriver2
    #将Chrome驱动文件路径赋给环境变量webdriver.chrome.driver

    driver = webdriver.Chrome(CDriver)
    #启动Chrome浏览器

    driver.maximize_window()
    #浏览器最大化

    driver.quit()
