
def power(x):
	if not isinstance(x,(int,float)):
		raise TypeError('bad operand Type')
	return x * x

#默认参数,必选参数在前，默认参数在后
def power_2(x,n=2):
	if not isinstance(x,(int,float)) or not isinstance(n,(int,float)):
		raise TypeError('bad operand Type')
	s = 1
	while n > 0:
		n = n - 1
		s = s * x
	return s

#默认参数必须指向不变对象
def add_end(L=[]):
	L.append('END')
	return L

def add_end_2(L=None):
	if L is None:
		L = []
	L.append('END')
	return L

#可变参数，函数调用时，自动组装为一个tuple
def calc(numbers):
	sum = 0
	for n in numbers:
		sum = sum + n * n
	return sum

def calc_2(*numbers):
	sum = 0
	for n in numbers:
		sum = sum + n * n
	return sum

#关键字参数，允许传入0个或任意个含参数名的参数，自动组装为一个dict
def person(name, age, **kw):
	print('name:', name,"age:", age, "other:", kw)

def person_2(name,age,**kw):
	if 'city' in kw:
		pass
	if 'job' in kw:
		pass
	print('name:', name,"age:", age, "other:", kw)

def person_3(name,age,*,city,job):
	print(name,age,city,job)

def person_4(name,age,*args,city,job):
		print(name,age,args,city,job)

#参数组合
def f1(a,b,c=0,*args,**kw):
	print('a=',a,'b=',b,'c=',c,'args=',args,'kw=',kw)

def f2(a,b,c=0,*,d,**kw):
	print('a=',a,'b=',b,'c=',c,'d=',d,'kw=',kw)

def main():
	power(2)
	print("2的平方：", power(2))

	print("x的立方：", power_2(2,3))
	print("x的n次方：", power_2(2))
	print("add_end()",add_end())
	print("add_end()",add_end())
	print("add_end_2()",add_end_2())
	print("add_end_2()",add_end_2())
	print("可变参数calc()", calc([1,2,3]))
	print("可变参数calc()", calc((1,2,3,7)))
	print("可变参数calc_2()", calc_2(1,2,3))
	print("可变参数calc_2()", calc_2(1,2,3,7))
	nums = [1,2,3]
	print("可变参数calc()",calc(nums))
	print("可变参数calc_2", calc_2(*nums))

	person('Bob', 35, city='Beijing')
	person('Adam', 45, gender='M', job='Engineer')
	extra = {'city':'Beijing', 'job':'Engineer'}
	person('Jack',24, **extra)
	person_2('Jack',24,city='Beijing',addr='Chaoyang',zipcode=123456)
	person_3('Jack',24,city='Beijing',job='Engineer')
	person_4('Jack',24,job='Engineer',city='Beijing')
	print('----------------------------')
	f1(1,2)
	f1(1,2,c=3)
	f1(1,2,3,'a','b')
	f1(1,2,3,'a','b',x=99)
	f2(1,2,d=99,ext=None)
	print('-----------------------------')
	args=(1,2,3,4)
	kw = {'d':99,'x':'#'}
	f1(*args,**kw)
	args2 = (1,2,3)
	kw2 = {'d':88,'x':'#'}
	f2(*args2,**kw2)



if __name__ == "__main__":
    main()