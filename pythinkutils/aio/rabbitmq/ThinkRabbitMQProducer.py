# -*- coding: utf-8 -*-

import asyncio
import asyncio
import aio_pika
import aio_pika.abc

# from pythinkutils.aio.common.aiolog import g_aio_logger

class ThinkRabbitMQProducer(object):
    g_dictConnPool = {}
    g_lock = asyncio.Lock()

    @classmethod
    async def conn(cls, szUrl, szQueue):
        szKey = "{}:{}".format(szUrl, szQueue)
        if cls.g_dictConnPool.get(szKey) is None:
            async with cls.g_lock:
                if cls.g_dictConnPool.get(szKey) is None:
                    try:
                        connection: aio_pika.RobustConnection = await aio_pika.connect_robust(szUrl, loop=asyncio.get_event_loop())
                        channel: aio_pika.abc.AbstractChannel = await connection.channel()

                        exchange = channel.default_exchange

                        cls.g_dictConnPool[szKey] = exchange
                    except Exception as e:
                        # await g_aio_logger.error(e)
                        return None

        exchange = cls.g_dictConnPool.get(szKey)
        return exchange