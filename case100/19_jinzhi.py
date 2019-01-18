# -*- coding: UTF-8 -*-
#转化进制数展示
 
# 获取用户输入十进制数
def is_number():
	while(1):
		try:
			n = int(input('请输入一个整数：'))
			return n
		except ValueError:
			print('输入错误')

dec = is_number()
 
print("十进制数为：", dec)
print("转换为二进制为：", bin(dec))
print("转换为八进制为：", oct(dec))
print("转换为十六进制为：", hex(dec))

#divmod()函数，返回一个包含商和余数的元组

def dec2bin(num):
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num))
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
            return ''.join(l[::-1])

def dec2oct(num):
    l = []
    if num < 0:
        return '-' + dec2oct(abs(num))
    while True:
        num, remainder = divmod(num, 8)
        l.append(str(remainder))
        if num == 0:
            return ''.join(l[::-1])


base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
def dec2hex(num):
    l = []
    if num < 0:
        return '-' + dec2hex(abs(num))
    while True:
        num,rem = divmod(num, 16)
        l.append(base[rem])
        if num == 0:
            return ''.join(l[::-1])

print("十进制数为：", dec)
print("转换为二进制为：", dec2bin(dec))
print("转换为八进制为：", dec2oct(dec))
print("转换为十六进制为：", dec2hex(dec))

