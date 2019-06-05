# -*- coding: UTF-8 -*-
# collections是Python内建的一个集合模块，提供许多有用的集合类

# namedtuple可以很方便地定义一种数据类型
from collections import namedtuple

# deque高效实现插入和删除操作的双向列表，适用队列和栈
from collections import deque

# defaultdict，字典dict的key不存在时，返回默认值
from collections import defaultdict

Point = namedtuple('Point',['x', 'y'])
p = Point(1, 2)
print(p.x)
print(p.y)

q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])