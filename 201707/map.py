#map函数接收两个参数，一个函数一个iterable，
#map将出入的函数一次作用在序列的每个元素，并把结果作为新的Iterator返回
def f(x):
	return x * x
r = map(f,[1,2,3,4,5,6,7,8,9])
print(list(r))

L = []
for n in [1,2,3,4,5,6,7,8,9]:
	L.append(f(n))
print(L)

print(list(map(str,[1,2,3,4,5,6,7,8,9])))

#reduce
from functools import reduce
def add(x,y):
	return x + y

print(reduce(add,[1,3,5,7,9]))

def fn(x,y):
	return x * 10 + y

print(reduce(fn,[1,3,5,7,9]))

def char2num(s):
	return{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]

print(reduce(fn,map(char2num,'13579')))	