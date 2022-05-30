# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://admin:123456@10.0.0.37/", loop=loop
    )

    async with connection:
        queue_name = "think-queue"

        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name
            , auto_delete=False
            , durable=True
        )

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()