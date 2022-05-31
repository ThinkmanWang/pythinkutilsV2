# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc

from pythinkutils.common.datetime_utils import *

async def main(loop):
    # Explicit type annotation
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
        "amqp://admin:123456@10.0.0.37", loop=loop
    )

    routing_key = "think-queue"

    channel: aio_pika.abc.AbstractChannel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=get_current_time_str().encode()
        ),
        routing_key=routing_key
    )

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
