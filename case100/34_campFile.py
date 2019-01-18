# -*- coding: UTF-8 -*-

# 比较两个文件，将不相同行，输出到另一个文件中
with open("1.csv", "rt") as in_file:
	text1 = in_file.read()

with open("2.csv", "rt") as in_file:
    text2 = in_file.read()

#读取文件内容，将内容以换行分隔为list
l1 = text1.split('\n')
l2 = text2.split('\n')

for i in range(0,len(l1)):
	if(l1[i] != l2[i]):
        # a+追加的方式写入文件
		with open("3.csv", "a+") as out_file:
			out_file.write(l1[i])
			out_file.write('\n')
			out_file.write(l2[i])