# -*- coding: utf-8 -*-

import time

from multiprocessing.pool import ThreadPool
from pythinkutils.common.log import g_logger

def foo(nNum):
  g_logger.info("%d" % (nNum,))

def main():
    pool = ThreadPool(processes=5)

    for i in range(100):
        pool.apply_async(foo, (i, ))

    time.sleep(5)

    for i in range(5):
        pool.apply_async(foo, (i, ))

    time.sleep(5)

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()