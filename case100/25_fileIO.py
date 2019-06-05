# -*- coding: UTF-8 -*-

import fileinput

# # 写文件
# with open("test.txt", "wt") as out_file:
#     out_file.write("该文本会写入到文件中\n看到我了吧！")
#
# Read a file
with open("a.txt", "rt") as in_file:
    text = in_file.read()

# 方法一：readline函数
f = open("a.txt")  # 返回一个文件对象  
line = f.readline() # 调用文件的 readline()方法  
while line:
    line = f.readline()
f.close()

# 方法二：一次读取多行
f = open("a.txt")
while 1:
    lines = f.readlines(7)
    if not lines:
        break
    for line in lines:
        print(line)
f.close()

# 方法三：直接for循环
for line in open("a.txt"):
    print(line)

# 方法四：使用fileinput
for line in fileinput.input("a.txt"):
    print(line)