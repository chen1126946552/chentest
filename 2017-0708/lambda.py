#匿名函数,就是没有函数名的函数
#只能有一个表达式，不用写return，返回值就是该表达式的结果
print(list(map(lambda x : x * x, [1,2,3,4,5,6,7,8,9])))

def f(x):
	return  x *ｘ

f1 = lambda x : x * x
print(f1) #f1是一个函数
print(f1(5)) # 25

#也可以把匿名函数作为返回值返回
def build(x,y):
	return lambda: x * x + y * y

print(build(2,3)) #build返回一个函数
print(build(2,3)()) #13 函数获取结果f()