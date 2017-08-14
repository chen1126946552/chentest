
#内置sorted函数
print(sorted([36,5,-12,9,-21])) #[-21, -12, 5, 9, 36]

#sorted函数也是高阶函数，可以接收一个key函数实现自定义的排序
#按照绝对值大小排序
print(sorted([36,5,-12,9,-21],key=abs)) #[5, 9, -12, -21, 36]

#默认情况下，对字符串排序，按照ASCII的大小比较
print(sorted(['bob','about','Zoo','Credit'])) #['Credit', 'Zoo', 'about', 'bob']

#忽略大小写排序
print(sorted(['bob','about','Zoo','Credit'],key=str.lower)) #['about', 'bob', 'Credit', 'Zoo']

#反向排序
print(sorted(['bob','about','Zoo','Credit'],key=str.lower,reverse=True)) #['Zoo', 'Credit', 'bob', 'about']


L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
#按照名字排序
def by_name(t):
	return t[0]
L2 = sorted(L,key=by_name)
print(L2)
	
def by_score(t):
	return t[1]
L3 = sorted(L,key=by_score,reverse=True)
print(L3)
