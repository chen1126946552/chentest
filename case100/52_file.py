# -*- coding: UTF-8 -*-

import json
import os

def test2():

    with open("a.txt", "rt") as in_file:
        text1 = in_file.read()

    # json.loads需要双引号，所以将字符串中的'替换成"
    test = text1.replace("\'", '\"')

    with open("a.csv", "w") as out_file:
        out_file.write('Status')
        out_file.write(',')
        out_file.write('templet_id')
        out_file.write(',')
        out_file.write('Create_Time')
        out_file.write(',')
        out_file.write('owner_id')
        out_file.write('\n')

    # 将字符串转成List, 里面是每个字典
    user_dict = json.loads(test)

    for i in user_dict:
        # a+追加的方式写入文件
        with open("a.csv", "a+") as out_file:
            out_file.write(str(i['Status']))
            out_file.write(',')
            out_file.write(i['templet_id'])
            out_file.write(',')
            out_file.write(str(i['Create_Time']))
            out_file.write(',')
            out_file.write(str(i['owner_id']))
            out_file.write('\n')


if __name__ == "__main__":
    error = './'+'test1.csv'
    fo = open(error, "a+")
    fo.write('test1'+'\n')
    a = fo.readlines()
    print(len(a))
    if (len(a) > 2):
        print(a)
    else:
        os.remove('test1.csv')

    fo.close()
