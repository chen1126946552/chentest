# -*- coding: UTF-8 -*-
#交换两个变量

def is_number():
	while(1):
		try:
			num = int(input('请输入一个数字: '))
			return num
		except ValueError:
			print("输入错误，请重新输入")

a = is_number()
b = is_number()

print('交换前两个变量为 %d,%d' %(a,b))

temp = a
a = b
b = temp

print('交换前两个变量为 %d,%d' %(a,b))

a,b = b,a
print('交换前两个变量为 %d,%d' %(a,b))

