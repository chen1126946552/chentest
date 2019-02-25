import unittest

def add(x,y):
    return x+y

class TestAdd(unittest.TestCase):

    def test_add(self):
        # 测试数据 1，2
        r = add(1,2) # 实际结果
        exp = 3 # 期望结果
        self.assertEqual(r, exp)

    def test_add2(self):
        r = add('hello','world')
        exp = 'helloworld'
        self.assertEqual(r,exp)

if __name__ == '__main__':
    unittest.main()

