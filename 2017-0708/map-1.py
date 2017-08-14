from functools import reduce

#lower函数：将字符串均变为小写
#capitalize函数：只将第一个字符大写，其他变为小写
def normalize(name):
	return  name.capitalize()
#另一种方法
#def normalize(name):
#	return name[0].upper() + name[1:].lower()

names = map(normalize,['adam','LISA','barT'])
print(list(names))

#返回列表中数字的乘积值
def prod(x,y):
	return x * y
p = reduce(prod,[3,5,7,9])
print('3 * 5 * 7 * 9 = ',p)

#将带小数点的字符串变为数值
def str2float(s):
	def char2num(s):
		return{'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
	#将字符串s按照.进行切分
	sp = s.split('.') # sp[0]='123' sp[1]='456'
	def f1(x,y):
		return x * 10 + y
	def f2(x,y):
		return x * 0.1 + y

	#将字符串sp[0] '123'变为数字123
	n1 = reduce(f1,map(char2num,sp[0])) 
	#sp[1][::-1]将sp[1]字符串倒序取,将字符串sp[1]'456'变为4.56
	n2 = reduce(f2,map(char2num,sp[1][::-1]))
	
	return n1 + n2 * 0.1

print(str2float('123.456'))
