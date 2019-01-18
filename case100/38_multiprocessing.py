# -*- coding: UTF-8 -*-

# 创建子线程函数fork()

import os

print('Process (%s) start...' % os.getpid())

# Only works on Unix/Linux/Mac:
pid = os.fork()
# 这个函数很特殊，调用一次，返回两次，
# 因为操作系统是将当前的进程（父进程）复制了一份（子进程），
# 然后分别在父进程和子进程内返回。子进程永远返回0，而父进程返回子进程的 PID
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))