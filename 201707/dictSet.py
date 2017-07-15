
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85} #d为一个字典dict
print (d['Michael'])

print ('Thomas' in d)

print (d.get('Thomas',-1))
print (d.get('Bob'))

d['Thomas'] = 78 #向d中插入一条记录
print(d)
d.pop('Bob') # 删除一条记录
print(d)

print('------------')
s = set(1,2,3) #s为一个 set

s1 = set([1, 1, 2, 2, 3, 3])
print(s1)
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)