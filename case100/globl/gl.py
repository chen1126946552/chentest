# -*- coding: utf-8 -*-

class Config_1:
    ABTEST = 1

class Config_2:
    ABTEST = 2

def _init():#初始化
    global a
    a = Config_1

def set_value(value):
    global a
    if value == 'Config_1':
        a = Config_1
    else:
        a = Config_2


def get_value():
    return a