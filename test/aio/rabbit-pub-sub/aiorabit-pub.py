# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc
from aio_pika import DeliveryMode, ExchangeType, Message, connect


from pythinkutils.common.datetime_utils import *

async def main() -> None:
    # Perform connection
    connection = await connect("amqp://admin:123456@10.0.0.37")

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        logs_exchange = await channel.declare_exchange(
            "fxxk", ExchangeType.FANOUT,
        )

        while True:
            message_body = get_current_time_str().encode()

            message = Message(
                message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            # Sending the message
            await logs_exchange.publish(message, routing_key="info")

            print(f" [x] Sent {message!r}")

            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
