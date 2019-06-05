# -*- coding: UTF-8 -*-

# 启用大量子进行，用进程池的方式

from multiprocessing import Pool
import os, time, random


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    # 最多同时执行4个进程，Pool的默认大小在我的电脑上是4
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))

    print('Waiting for all subprocesses done...')
    # 调用close()之后就不能继续添加新的Process了
    p.close()
    # 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()
    p.join()
    print('All subprocesses done.')
