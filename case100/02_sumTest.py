# -*- coding: UTF-8 -*-

# 求两个数字之和

#第一种方法：默认输入正确
#num1 = input('输入第一个数字：')
#num2 = input('输入第二个数字：')

#input输入为字符串，需要用float方法将字符串转化为浮点数类型
#sum1 = float(num1) + float(num2)

#print('数字 %s 和 %s 的和为 %f' %(num1,num2,sum1))

#第二种方法: 兼容输入错误情况
'''
num1 = input('输入第一个数字: ')
while(1):
	try:
		n1 = float(num1)
		break
	except ValueError:
		print("输入错误，请输入一个数字")
		num1 = input('输入第一个数字: ')

num2 = input('输入第二个数字： ')
while(1):
	try:
		n2 = float(num2)
		break
	except ValueError:
		print("输入错误，请输入一个数字")
		num2 = input('输入第一个数字: ')

print('数字 %s 和 %s 的和为 ' %(num1,num2,n1+n2))
'''
#可以做多个数值，加减乘除





