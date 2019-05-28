import unittest

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('所有用例之前只准备一次')

    @classmethod
    def setUp(self):
        print('每条用例执行之前都会执行')

    @classmethod
    def tearDown(self):
        print('每条用例执行之后都会执行')

    @classmethod
    def tearDownClass(cls):
        print('所有用例之后只执行一次')

    def test_01(self):
        print("测试用例1")

    def test_02(self):
        print("测试用例2")

if __name__ == '__main__':
    unittest.main()