#切片
L = ['Michael', 'Sarah','Bob', 'Jack']
print(L[0:3])
print(L[-2:])
L1 = list(range(100))
print(L1)
#前10
print(L1[:10])
#后10
print(L1[-10:])
#前11-20
print(L1[10:20])
#前10个数，每两个取一个
print(L1[:10:2])
#所有数，每5个取一个
print(L1[::5])
#原样
print(L1[:])

#tuple
T = (0,1,2,3,4,5)
print(T[:3])
print('ABCDEFG'[:3])
print('ABCDEFG'[::2])
