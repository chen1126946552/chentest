#一般的求和函数定义
def calc_sum(*args):
	ax = 0
	for n in args:
		ax = ax + n
	return ax

#返回求和的函数
def lazy_sum(*args):
	def sum():
		ax = 0
		for n in args:
			ax = ax + n
		return ax
	return sum 

f = lazy_sum(1,3,5,7,9)
#f是一个函数
print(f) #<function lazy_sum.<locals>.sum at 0x101c6ed90>
#调用函数f,返回结果
print(f()) #25

#每次调用均会返回一个新的函数,且二者不互相影响
f1 = lazy_sum(1,3,5,7,9)
print (f == f1) #False

#返回函数不要引用任何循环变量，或者后续会发生变化的变量。
def count():
	fs = []
	for i in range(1,4):
		def f():
			return i * i
		fs.append(f)
	return fs
f1,f2,f3 = count()
print(f1(),f2(),f3()) # 9,9,9
#原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。

def count2():
	def f(j):
		def g():
			return j*j
		return g
	fs = []
	for i in range(1,4):
		fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
	return fs
f1,f2,f3 = count2()
print (f1(),f2(),f3()) #1,4,9
