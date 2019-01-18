# -*- coding: UTF-8 -*-
#通过用户输入数字计算阶乘


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


def is_factorial(n):
	if n == 0:
		return 1
	else:
		num = 1
		for n1 in range(1,n+1):
			num *= n1
		return num


n = is_number()
print(is_factorial(n))
