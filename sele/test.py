import os

import time
import getbrowser  #引入Getbrowser，以便调用不同的浏览器
import unittest #引入unittest单元测试框架

class RunSogou(unittest.TestCase): # 新建一个unittest的TestCase的类
    def setUp(self): # 运行测试用例前需要执行的方法
        self.driver = getbrowser.Chrome()
# 调用Getbrowser的Chrome浏览器,也可调用IE,Firefox浏览器

    def testRunSogou(self): #测试用例主方法,必须以test开头命名,否则无法运行
        driver = self.driver
        driver.get("http://www.sogou.com")
        time.sleep(2)
        self.assertIn('搜狗搜索',driver.title)
        time.sleep(2)
# 以上方法为打开搜狗主页，并验证网页标题正确与否，涉及的代码会在后续章节”常见使用方法”，详细说明，这里只需了解即可

    def tearDown(self): #运行测试用例完毕后执行的方法
        self.driver.quit() #退出浏览器

if __name__ == '__main__':
    unittest.main() #执行unittest的主方法，则会运行上述脚本