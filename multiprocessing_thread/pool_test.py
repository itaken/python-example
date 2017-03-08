#! /usr/bin/python3
from multiprocessing import Pool
import os, time, random

'''
   进程池
   @since 2017-03-08
   @link http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000
'''


def run_task(name):
    time.sleep(random.random() * 2)  # 将进程sleep,模拟程序运行,方便查看效果
    print("任务 %s 运行在进程 %s" % (name, os.getpid()))


if __name__ == '__main__':
    print("当前进程是: %s" % os.getpid())
    pl = Pool(4)
    for i in range(5):
        pl.apply_async(func=run_task, args=(i,))
    print("等待子进程...")
    pl.close()
    pl.join()
    print("子进程结束.")
