# -*- coding: UTF-8 -*-

#如果一个n位正整数等于其各位数字的n次方之和,则称该数为阿姆斯特朗数。 
#例如1^3 + 5^3 + 3^3 = 153。


def is_number():
	while(1):
		try:
			n = int(input('请输入一个整数：'))
			if n > 0:
				return n
			else:
				print('输入错误')
		except ValueError:
			print('输入错误')

n = is_number()
nlen = len(str(n))

#总和值
nsum = 0

n1 = n
for i in range(1,nlen+1):
	temp = n1 % 10
	nsum += temp ** nlen
	n1 //= 10
	
if nsum == n:
	print('阿姆斯特朗数')
else:
	print('不是阿姆斯特朗数')
