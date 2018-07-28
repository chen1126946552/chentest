#filter()也接收一个函数和一个序列，把传入的函数依次作用于每个元素，根据返回值true还是false决定保留还是丢弃

#在一个list中，删掉偶数，只保留奇数
def is_odd(n):
	return n % 2 == 1
print (list(filter(is_odd,[1,2,4,5,6,9,15]))) #[1, 5, 9, 15]

#将序列中的空字符串删掉
def not_empty(s):
	return s and s.strip() #strip()删除字符串中空白符，strip(rm)删除字符串开头结尾为rm的字符，lstrip(rm) 删除开头为rm, rstrip(rm)删除结尾为rm
print(list(filter(not_empty,['A','','B',None,'C',' ']))) #['A','B','C']


#计算素数
#1、先定义一个从3开始的奇数序列,此函数是一个生成器，并且是一个无限序列
def _odd_iter():
	n = 1
	while True:
		n = n + 2
		yield n

#2、定义一个筛选器
def _not_divisible(n):
	return lambda x : x % n > 0

#3、定义一个生成器，不断返回下一个素数
def primes():
	yield 2
	it = _odd_iter() #初始序列
	while True:
		n = next(it) #返回序列中的第一个数
		yield n 
		it = filter( _not_divisible(n), it) #构造新序列

for n in primes():
	if n < 1000:
		print(n)
	else:
		break

#过滤掉不是回数的数，回数：从左往右与从右往左是一样的
def is_palindrome(n):
	return int(str(n)[::-1]) == n
output = filter(is_palindrome,range(1,1000))
print(list(output))

