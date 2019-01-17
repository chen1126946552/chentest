#包，每个包下面必须有一个__init__.py的文件, 否则会认为目录是普通目录
#创建模块时，不能和Python自带的模块名称冲突
# !/usr/bin/env python3
# -*- codidng: utf-8 -*-
'a test module'

__author__ = 'chen.chen'

import  sys

def test():
	args = sys.argv
	if len(args) == 1
		print('Hello,world!')
	elif len(args) == 2
		print('Hello ,%s!' %args[1])
	else:
		print('Too many arguments!')

if __name__ =='__main__':
	test()