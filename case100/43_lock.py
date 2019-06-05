# -*- coding: UTF-8 -*-

# 添加lock，确保修改正确

import time, threading

# 假定这是银行存款：
balance = 0
balance2 = 0
lock = threading.Lock()


def change_it(n):
    # 先存后取，结果应该为0
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(100000):
        change_it(n)


# 通过上锁，确保修改正确
def run_thread2(n):
    for i in range(100000):
        # 先获取锁:
        lock.acquire()
        # 通过try finally来确保锁一定会被释放，避免成为死线程
        try:
            # 放心修改
            change_it(n)
        finally:
            # 改完释放锁
            lock.release()


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

t3 = threading.Thread(target=run_thread2, args=(5,))
t4 = threading.Thread(target=run_thread2, args=(8,))
t3.start()
t4.start()
t3.join()
t4.join()
print(balance2)
