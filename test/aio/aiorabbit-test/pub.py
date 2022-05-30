# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc
from aio_pika import DeliveryMode, ExchangeType, Message, connect

from pythinkutils.aio.rabbitmq.ThinkRabbitMQPub import ThinkRabbitMQPub
from pythinkutils.common.datetime_utils import *
from pythinkutils.aio.common.aiolog import g_aio_logger

async def main():
    conn = await ThinkRabbitMQPub.conn("amqp://admin:123456@10.0.0.37/", "fxxk")

    for i in range(10):
        message_body = get_current_time_str().encode()

        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        # Sending the message
        await conn.publish(message, routing_key="info")

        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
