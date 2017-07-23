#生成器：不创建完整的list，节省大量的空间的，一边循环一边计算的机制
#把列表生成式的[]修改为(),即可

g = (x * x for x in range(10))
#print(g)  无法直接打印g
print(next(g))

for n in g:
	print(n)

def fib(max):
	n, a, b = 0, 0, 1
	while n < max:
		print(b)
		a, b = b , a+b
		n = n + 1
	return 'done'

#把fib函数变为generator,如果函数定义中包含yield，则这个函数为generator
def fib_2(max):
	n, a, b = 0, 0, 1
	while  n < max:
		yield b
		a, b = b, a+b
		n = n + 1
	return 'done'
		
fib(6)
g = fib_2(6)
while True:
	try:
		x = next(g)
		print('g:',x)
	except StopIteration as e:
		print('Generator return value:', e.value)
		break