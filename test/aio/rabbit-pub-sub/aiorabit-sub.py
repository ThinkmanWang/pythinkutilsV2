# -*- coding: utf-8 -*-
import asyncio
import aio_pika
import aio_pika.abc
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(f"[x] {message.body!r}")


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://admin:123456@10.0.0.37/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        logs_exchange = await channel.declare_exchange(
            "fxxk", ExchangeType.FANOUT,
        )

        # Declaring queue
        queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await queue.bind(logs_exchange)

        # Start listening the queue
        await queue.consume(on_message)

        print(" [*] Waiting for logs. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())