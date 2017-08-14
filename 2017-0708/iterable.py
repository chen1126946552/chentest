from collections import Iterable
from collections import Iterator

#可以直接作用与for循环的对象统称为可迭代对象iterable
print(isinstance([],Iterable))
print(isinstance((),Iterable))
print(isinstance({},Iterable))

print(isinstance('ABC',Iterable))
print(isinstance((x for x in range(10)),Iterable))

print(isinstance(100,Iterable))
print('-------------')
#可以被next()函数调用并不断返回下一个值饿对象称为迭代器Iterator
print(isinstance((x for x in range(10)),Iterator))
print(isinstance([],Iterator))
print(isinstance({},Iterator))
print(isinstance('abc',Iterator))

print('----------------')
print(isinstance(iter([]),Iterator))
print(isinstance(iter('abc'),Iterator))
print('---------')
for x in [1,2,3,4,5]:
	pass

#首先获得Iteratior对象
it = iter([1,2,3,4,5])
while True:
	try:
		#获得下一个值
		x = next(it)
	#遇到StopIteration就退出循环
	except StopIteration:
		break