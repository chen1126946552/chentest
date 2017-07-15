import math

def my_abs(x):
	if not isinstance(x,(int,float)):
		raise TypeError('bad operand Type')
	if x >= 0:
		return x
	else:
		return -x

#空函数，什么事也不做
def nop():
		pass

#返回一元二次方程的解
def quadratic(a,b,c)

