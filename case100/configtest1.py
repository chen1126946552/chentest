# -*- coding: UTF-8 -*-

class Config_1:
    ABTEST = 1

class Config_2:
    ABTEST = 2


global val  # 在使用前初次声明
val = 10  # 给全局变量赋值


def xy():
    global val  # 再次声明，表示在这里使用的是全局变量，而不是局部变量
    val += 12
    print('现在是全局变量val,值为', val)


def zoo():
    val = 5
    print('现在是局部变量val,值为', val)


if __name__ == "__main__":
    xy()
    zoo()