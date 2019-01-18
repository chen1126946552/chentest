# -*- coding: UTF-8 -*-
#生成随机数

import random

i = 1
#生成0-100之间的随机整数
a = random.randint(0,100)

def is_number():
	while(1):
		try:
			num = int(input('请输入一个0-100的数字: '))
			return num
		except ValueError:
			print("请再次输入一个数")

b = is_number()

while a != b:
	if a > b:
		print('你输入的数字小于随机数字')
		b = is_number()
	else:
		print('你输入的数字大于随机数字')
		b = is_number()
	i += 1
else:
	print('恭喜你，猜对了')
