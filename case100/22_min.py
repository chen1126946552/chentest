# -*- coding: UTF-8 -*-

#最小公倍数

a,b = input("请输入2个数字(空格分隔)：").split()

n1 = int(a)
n2 = int(b)


def testmax(a,b):
	c = max(a,b)
	while(1):
		if((c%a == 0) and (c%b == 0)):
			return c
		c += 1

print(testmax(n1,n2))