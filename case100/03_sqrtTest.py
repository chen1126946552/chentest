# -*- coding: UTF-8 -*-

#求平方根

#第一种方法：乘以0.5
'''
num = float(input('请输入一个数字： '))
num_sqrt = num ** 0.5
print('%0.3f 的平方根为 %0.3f' %(num,num_sqrt))
'''
#第二种方法：数学公式
#计算实数和负数平方根
'''
import cmath

num = int(input('请输入一个数字： '))
num_sqrt = cmath.sqrt(num)
print('{0} 的平方根为 {1:0.3f}+{2:0.3f}j'.format(num ,num_sqrt.real,num_sqrt.imag))
'''
#第三种：兼容输入错误
import cmath

while(1):
	try:
		num = int(input('请输入一个数字: '))
		break
	except ValueError:
		print("输入错误，请输入一个整数")
num_sqrt = cmath.sqrt(num)
print('{0} 的平方根为 {1:0.3f}+{2:0.3f}j'.format(num ,num_sqrt.real,num_sqrt.imag))
