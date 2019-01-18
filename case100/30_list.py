# -*- coding: UTF-8 -*-
#list常用操作

#list定义
li = ["a", "b", "mpilgrim", "z", "example"]
print(li[1])

#负数索引

print(li[-1])

print(li[-3])

pirnt(li[1:3])

print(li[1:-1])

print(li[0:3])

#list增加元素
li.append('new')
print(li)

li.insert(2,'new2')
print(li)

li.extend('new3','elements')
print(li)

#list检索

print(li.index('example'))

#list删除元素
print(li.remove('z'))
print(li)

print(li.pop())
print(li)


#list运算符
li = li + ['example', 'new']
print(li)

li += ['two']
print(li)

li = [1,2] * 3
print(li)