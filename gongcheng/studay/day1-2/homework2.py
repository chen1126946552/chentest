# -*- coding: UTF-8 -*-

# 打印99乘法表
def test(a):
    for i in range(1, a + 1):
        for j in range(1, i + 1):
            print('{0} * {1} = {2}'.format(i, j, i * j), end='  ')
        print()


if (__name__ == "__main__"):
    test(9)
