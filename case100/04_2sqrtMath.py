# -*- coding: UTF-8 -*-

#计算二次方程式: ax**2 + bx + c = 0
# a,b,c 用户提供，为实数，a != 0

'''
import cmath

a = float(input('输入 a : '))
b = float(input('输入 b : '))
c = float(input('输入 c : '))

d = (b**2) - (4*a*c)

sol1 = (-b - cmath.sqrt(d)) / (2*a)
sol2 = (-b + cmath.sqrt(d)) / (2*a)

print('结果为 {0} 和 {1}' .format(sol1,sol2))
'''
import math

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

d = (b**2) - (4*a*c)

if a == 0 and b == 0 :
	print('不是方程式，不需要解')

elif a == 0 and b != 0 :
  print("一次方程式，x 结果为： %0.2f" %(-c/b))

elif a !=0 and b == 0 :
	if d >= 0 :
		print("一次方程式，x 结果为：%0.2f" %(math.sqrt(-c/a)))
	else:
		print('方程式，无解')
elif d >= 0:
  x1 = (-b-d/(2*a))
  x2 = (-b+d/(2*a))
  print('结果为：%.2f,%.2f'%(x1,x2));
else:
  print("无解")