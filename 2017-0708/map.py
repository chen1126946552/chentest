#map函数接收两个参数，一个函数一个iterable，
#map将出入的函数一次作用在序列的每个元素，并把结果作为新的Iterator返回
def f(x):
	return x * x
r = map(f,[1,2,3,4,5,6,7,8,9])
print(list(r))  #[1, 4, 9, 16, 25, 36, 49, 64, 81]

#for循环添加到数组
L = []
for n in [1,2,3,4,5,6,7,8,9]:
	L.append(f(n))
print(L) #[1, 4, 9, 16, 25, 36, 49, 64, 81]

#将数字变为字符串，存储在list中
print(list(map(str,[1,2,3,4,5,6,7,8,9]))) #['1', '2', '3', '4', '5', '6', '7', '8', '9']

#reduce, 必须接收两个参数，把结果继续和序列的下一个月按时做累积计算
from functools import reduce
def add(x,y):
	return x + y

print(reduce(add,[1,3,5,7,9])) # 1+3+5+7+9 = 25


def fn(x,y):
	return x * 10 + y

print(reduce(fn,[1,3,5,7,9]))
# (((x*10 + 3)*10 + 5)*10 +7)*10 +9 = 13579


def char2num(s):
	return{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]

#先把字符串转化为数字序列，再调用fn函数
print(reduce(fn,map(char2num,'13579')))	# (((x*10 + 3)*10 + 5)*10 +7)*10 +9 = 13579