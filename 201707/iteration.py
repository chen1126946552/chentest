#迭代
d = {'a':1,'b':2,'c':3}

#迭代key
for key in d:
	print(key)
print('---------')

#迭代Value
for value in d.values():
	print(value)

print('----------')
#同时迭代key和value
for k,v in d.items():
	print(k,':',v)

print('-----------')

for ch in 'ABC':
	print(ch)
print('-----------')

from collections import Iterable
print(isinstance('abc',Iterable))  #str是否可迭代,可以
print(isinstance([1,2,3],Iterable)) #list是否可迭代，可以
print(isinstance(123,Iterable)) #整数是否可迭代，不可以
print('-----------')

#对list实现类似java中下标循环
for i, value in enumerate(['A','B','C']):
	print(i, value)
print('-----------')

for x, y in [(1,2),(2,4),(3,9)]:
	print(x, y)