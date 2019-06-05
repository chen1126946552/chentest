# -*- coding: UTF-8 -*-
#判断是否为闰年

def is_year():
	while(True):
		try:
			s = int(input('请输入一个年份数字: '))
			if s <= 0:
				print('请输入大于0的年份!!!')
			else:
				return s
		except ValueError:
			print('请输入正确年份数字!!!')


def is_runyear(s):
	if(s % 4) == 0 :
		if (s % 100) == 0:
			if(s % 400) == 0:
				print('{0} 是闰年' .format(s))
			else:
				print('{0} 不是闰年' .format(s))
		else:
			print('{0} 是闰年' .format(s))
	else:
		print('{0} 不是闰年' .format(s))


s = is_year()
is_runyear(s)
