#函数是一个对象，可以通过赋值给变量，通过变量进行调用
def now():
	print('2015-3-25')

f = now
f()

#函数对象的_name_熟悉，可以拿到函数的名字
a = now.__name__
print(a)

b = f.__name__
print(b)

#装饰器：在代码运行期间动态增加功能的方式
#本质上装饰器decorator就是一个返回函数的高阶函数
#定义一个打印日志的decorator
def log(func):
	def wrapper(*args,**kw):
		print('call %s():' %func.__name__)
		return func(*args,**kw)
	return wrapper

@log
def now1():
	print('2015-3-25')

now1() #call now1() \n 2015-3-25

#decorator本身需要传人参数，就需要编写一个返回decorator的高阶函数
def log(text):
	def decorator(func):
		def wrapper(*args,**kw):
			print('%s %s():' % (text,func.__name__))
			return func(*args,**kw)
		return wrapper
	return decorator

@log('execute')
def now():
	print('2015-3-25')

now()  #execute now() \n  2015-3-25
print(now.__name__) #'wrapper'

#内置函数wraps就是将wrapper.__name__ = func.__name__
#完整代码如下
import functools
def log(func):
	@functools.wraps(func)
	def wrapper (*args, **kw):
		print('call %s():' % func.__name__)
		return func(*args,**kw)
	return wrapper

#带参数的
import functools
def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('%s %s():' %(text,func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

#在函数调用前后分别打印内容，且支持无参数和有参数
import functools
def log1(*text):
	def decorator(func):		
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('begin call')
			if (len(text) > 0):
				print('%s %s():' %(*text,func.__name__)) 
			else:
				print('%s'%func.__name__)
			func(*args, **kw)
			print('end call')
		return wrapper	
	return decorator

#@log1('execute')
@log1()
def f():
	pass

f()

			











