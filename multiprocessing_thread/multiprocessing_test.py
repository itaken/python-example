#! /usr/bin/python3
from multiprocessing import Process
import os

'''
   多进程
   @since 2017-03-07
   @link http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000
'''


def run_something(name):
    print("这里使用 %s进程 处理 %s." % (os.getpid(), name))


if __name__ == '__main__':
    print("当前进程是: %s" % os.getpid())
    pro = Process(target=run_something, args=('Hello',))
    pro.start()
    pro.join()
    print("子进程结束.")
