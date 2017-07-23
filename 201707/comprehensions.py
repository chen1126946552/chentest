#列表生成器,可以用来创建list的生成式

print(list(range(1,11)))

L = []
for x in range(1,11):
	L.append(x * x)
print(L)

L2 = [x * x for x in range(1,11)]
print(L2)

L3 = [x * x for x in range(1,11) if x % 2 == 0]
print(L3)

L4 = [m + n for m in 'ABC' for n in 'XYZ']
print(L4)

d = {'x':'A','y':'B','z':'C'}
L5 = [k + '=' + v for k, v in d.items()]
print(L5)

L6 = ['Hello','World','IBM','Apple']
L7 = [s.lower() for s in L6]
print(L7)

#判断是否为字符串
x = 'abc'
y = 123
print(isinstance(x,str))
print(isinstance(y,str))

L8 = ['Hello','World','IBM',222,'Apple']
L9 = [s.lower() for s in L8 if isinstance(s,str)]
print(L8)

