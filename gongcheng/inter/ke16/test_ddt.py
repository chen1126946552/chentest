
import ddt
import unittest

# 准备的测试数据
dates = [
    {'user': 'admin1', 'psw': '111111', 'expect': True},
    {'user': 'admin2', 'psw': '222222', 'expect': True},
    {'user': 'admin3', 'psw': 'XXXXXX', 'expect': False},
]

@ddt.ddt
class TestLogin(unittest.TestCase):
    # @ddt.data({'user': 'admin1', 'psw': '111111', 'expect': True},
    # {'user': 'admin2', 'psw': '222222', 'expect': True},
    # {'user': 'admin3', 'psw': 'XXXXXX', 'expect': False},)
    @ddt.data(*dates)
    def test_01(self, testdata):
        print(testdata)
        user = testdata['user']
        pws = testdata['psw']
        exp = testdata['expect'] # 期望结果
        act = 'True' # 获取实际结果
        self.assertEqual(exp, act)

if __name__ == "__main__":
    unittest.main()

