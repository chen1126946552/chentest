# -*- coding: UTF-8 -*-

# 子进程
# subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出

import subprocess

print('$ python3 39_pool.py')
# 相当于在控制台输入命令 python3 39_pool.py
r = subprocess.call(['python3', '39_pool.py'])
print('Exit code:', r)

print('-------分隔线--------')
# 可以通过communicate()方法输入，子进程的输入内容
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)