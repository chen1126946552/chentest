# -*- coding: UTF-8 -*-
#判断是否为质数

import math

def is_prime(n):
	if n == 1:
		return False
	for i in range(2,int(math.sqrt(n) + 1)):
		if n % i == 0:
			return False
	return True


def is_number():
	while(1):
		try:
			n = int(input('请输入一个整数：'))
			if n >= 0:
				return n
			else:
				print('输入错误')
		except ValueError:
			print('输入错误')


n = is_number()
if (is_prime(n)):
	print('数值{0} 是质数' .format(n))
else:
	print('数值{0} 不是质数' .format(n))