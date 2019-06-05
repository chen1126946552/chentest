# -*- coding: UTF-8 -*-

#斐波那契数列实现


#获取输入整数函数
def is_number():
	while(1):
		try:
			n = int(input('请输入数列需要几项数字：'))
			if n > 0:
				return n
			else:
				print('输入错误')
		except ValueError:
			print('输入错误')

#递归
def fab(n):
	if n == 1:
		return 0
	if n == 2:
		return 1
	if n > 2:
		return fab(n-1) + fab(n-2)

def shulie(n):
	for i in range(1,n+1):
		print(fab(i),end=' ')


n = is_number()
#递归
if n == 1:
	print(0,end=' ')
else:
	shulie(n)

print()

print('----循环-----')
n1 = 0
n2 = 1
#循环
for i in range(1,n+1):
	if i == 1:
		print(n1,end=' ')
	else:
		print(n2,end=' ')
		n1,n2 = n2,n1
		n2 += n1
print()


