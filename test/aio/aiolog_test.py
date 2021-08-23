# -*- coding: utf-8 -*-
import asyncio
from pythinkutils.aio.common.aiolog import g_aio_logger

async def main():
    await g_aio_logger.debug("FXXK")
    await g_aio_logger.info("FXXK")
    await g_aio_logger.info("FXXK1")

if __name__ == '__main__':
    asyncio.run(main())