# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc
from aio_pika import DeliveryMode, ExchangeType, Message, connect

from pythinkutils.aio.rabbitmq.ThinkRabbitMQPub import ThinkRabbitMQPub
from pythinkutils.common.datetime_utils import *
from pythinkutils.aio.common.aiolog import g_aio_logger
from pythinkutils.config.Config import ThinkConfig

async def main():
    conn = await ThinkRabbitMQPub.conn(ThinkConfig.get_default_config().get("rabbitmq", "url"), ThinkConfig.get_default_config().get("rabbitmq", "broadcast"))

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
