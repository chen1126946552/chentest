# -*- coding: UTF-8 -*-
#摄氏温度转成华式温度 F = (c * 1.8) +32

def is_number():
	while(1):
		try:
			num = float(input('请输入摄氏温度: '))
			return num
		except ValueError:
			print("输入错误，请重新输入")

celsius = is_number()

fahrenheit = (celsius * 1.8) + 32
print('%0.1fC 摄氏温度转为华氏温度为 %0.1fF' %(celsius,fahrenheit))
