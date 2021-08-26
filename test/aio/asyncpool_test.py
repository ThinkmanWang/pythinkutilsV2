# -*- coding: utf-8 -*-

import asyncio
from asyncio_pool import AioPool

from pythinkutils.aio.common.aiolog import g_aio_logger

async def cor_worker(nNum):
    while True:
        await g_aio_logger.info("FXXK %d" % (nNum, ))
        await asyncio.sleep(5)


async def start_pool(nSize):
    pool = AioPool(size=nSize)

    for i in range(nSize):
        pool.spawn_n(cor_worker(i))

    await pool.join()

async def test1():
    await g_aio_logger.info("FXXXXXXXXXXXXK")

def main():
    loop = asyncio.get_event_loop()
    asyncio.gather(start_pool(5))
    asyncio.gather(test1())
    loop.run_forever()

if __name__ == '__main__':
    main()