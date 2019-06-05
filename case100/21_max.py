# -*- coding: UTF-8 -*-

#最大公约数

a,b = input("请输入2个数字(空格分隔)：").split()

n1 = int(a)
n2 = int(b)


def testmax(a,b):
	c = min(a,b)
	while(c):
		if((a%c == 0) and (b%c == 0)):
			return c
		c -= 1

print(testmax(n1,n2))