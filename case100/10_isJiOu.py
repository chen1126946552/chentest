# -*- coding: UTF-8 -*-
#判断奇数偶数

def is_number():
	while(1):
		try:
			s = int(input('请输入一个整数:'))
			return s
		except ValueError:
			print('输入不符合条件')

def is_jiou(s):
	if(s % 2 == 0):
		print('数字 %d 是偶数' %s)
	else:
		print('数字 %d 是奇数' %s)


s = is_number()
is_jiou(s)
