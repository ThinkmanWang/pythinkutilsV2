# -*- coding: utf-8 -*-

import asyncio

import asyncio
import aio_pika
import aio_pika.abc

from pythinkutils.aio.rabbitmq.ThinkRabbitMQProducer import ThinkRabbitMQProducer
from pythinkutils.common.datetime_utils import *
from pythinkutils.aio.common.aiolog import g_aio_logger

async def main():
    for i in range(10):
        routing_key = "think-queue"
        conn = await ThinkRabbitMQProducer.conn("amqp://admin:123456@10.0.0.37", routing_key)
        await g_aio_logger.info("%s" % (conn, ))

        await conn.publish(
            aio_pika.Message(
                body=get_current_time_str().encode()
            ),
            routing_key=routing_key
        )

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
