# -*- coding: UTF-8 -*-
# 求1000以内的水仙花数

import math


# 获取数值的每一位
def test3(n):
    x = n
    li = []
    i = 0
    sum1 = 0
    while(int(x)):
        li.append(int(x % 10))
        x /= 10
        i += 1
    for j in li:
        sum1 = sum1 + pow(j,i)
    if int(sum1) == int(n):
        return 1
    return 0
if (__name__ == "__main__"):
    for i in range(100,1000):
        if(test3(i) == 1):
            print(i)