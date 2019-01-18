# -*- coding: UTF-8 -*-
#输出指定范围内的素数

import math

#判断是否为质数函数
def is_prime(n):
	if n == 1:
		return False
	for i in range(2,int(math.sqrt(n) + 1)):
		if n % i == 0:
			return False
	return True

#获取输入整数函数
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

n1 = is_number()
n2 = is_number()

for num in range(min(n1,n2), max(n1,n2)+1):
	if (is_prime(num)):
		print('数值{0} 是质数' .format(num))
	else:
		print('数值{0} 不是质数' .format(num))