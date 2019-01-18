#装饰器
import functools

def now():
	print('2019-3-25')

now()
print('----------------')
def log(text):
	def decorator(func):
		def wrapper(*args,**kw):
			print('%s %s():' %(text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

@log('execute')
def now1():
	print('2019-3-26')

now1()
print('-------------')

nowtest2 = log('execute')(now1)
nowtest2()
print('------------------')
print(nowtest2.__name__)


def log2(text):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		print('call %s():' % func.__name__)
		return func(*args, **kw)
	return wrapper

@log2('execute')
def now2():
	print('2019-3-27')

nowtest3 = log2('execute')(now2)
print(nowtest3.__name__)		

