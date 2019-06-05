# -*- coding: UTF-8 -*-
# 通过三角形的三边长度，计算三角形的面积
# s = (a + b + c) / 2
# area = sqrt(s * (s-a) * (s-b) * (s-c))


import math

#定义输入数值函数
def is_number():
	while(1):
		try:
			num = float(input('请输入一个数字: '))
			return num
		except ValueError:
			print("输入错误，请输入一个数")

a = is_number()
b = is_number()
c = is_number()

s = (a + b + c) / 2

area = math.sqrt(s * (s-a) * (s-b) * (s-c))

print('三角形面积为 %0.2f' %area)