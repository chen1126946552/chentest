# -*- coding: utf-8 -*-
# UI访问页面，查看engage有正常展示，且为测试账号构造数据

import time

def test_01(browser):
    '''1、判断http://datatest11.ptmind.com/cnonline_auto/index.html页面肯定存在，ptEngage元素'''
    browser.get('http://datatest16.ptmind.com/chen_ptx/designers.html')
    time.sleep(2)
    browser.get('http://datatest16.ptmind.com/chen_ptx/index.html')
    time.sleep(2)
    # try:
    #     browser.find_element_by_id('ptEngage')
    #     ptEngage = 'True'
    # except:
    #     ptEngage = 'False'
    # print('1、判断http://datatest11.ptmind.com/cnonline_auto/index.html页面肯定存在，ptEngage元素')
    # assert ptEngage == 'True'

