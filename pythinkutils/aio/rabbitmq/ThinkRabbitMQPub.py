# -*- coding: utf-8 -*-

import asyncio
import asyncio
import aio_pika
import aio_pika.abc
from aio_pika import DeliveryMode, ExchangeType, Message, connect


class ThinkRabbitMQPub(object):
    g_dictConnPool = {}
    g_lock = asyncio.Lock()

    @classmethod
    async def conn(cls, szUrl, szQueue):
        szKey = "{}:{}".format(szUrl, szQueue)
        if cls.g_dictConnPool.get(szKey) is None:
            async with cls.g_lock:
                if cls.g_dictConnPool.get(szKey) is None:
                    try:
                        connection = await connect(szUrl)

                        channel = await connection.channel()

                        exchange = await channel.declare_exchange(
                            szQueue, ExchangeType.FANOUT,
                        )

                        cls.g_dictConnPool[szKey] = exchange
                    except Exception as e:
                        # await g_aio_logger.error(e)
                        return None

        exchange = cls.g_dictConnPool.get(szKey)
        return exchange
