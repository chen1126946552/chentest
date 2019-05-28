# -*- coding: UTF-8 -*-

# 排序
def sort1(a):
    for i in range(len(a)):
        for j in range(i, len(a)):
            if a[j] <= a[i]:
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
    return a

# 去重
def quchong(a):
    new = []
    for i in a:
        if i not in new:
            new.append(i)
    return new

# 计算出现次数
def count1(a):
    dic = {}
    for i in a:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    return dic




if ( __name__ == "__main__"):
    a = [1, 6, 8, 11, 9, 1, 8, 6, 8, 7, 8]

    print(sort1(a))  # 将list进行排序，从小到大
    print(quchong(a)) # 去掉重复出现的数字
    c = count1(a)  # 获得每个数字出现的重复次数
    print(c)

    print(max(c, key = c.get)) # 获得重复次数最多的值
    print(max(c.values())) #获得最多的重复次数