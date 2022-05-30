# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc
from abc import *
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

class ThinkRabbitMQSub(object):
    __metaclass__ = ABCMeta

    def __init__(self, szUrl, szQueue):
        self.m_szUrl = szUrl
        self.m_szQueue = szQueue
        self.m_bStarted = False

    def start(self):
        if self.m_bStarted:
            return

        asyncio.gather(self.on_start())

        self.m_bStarted = True

    @abstractmethod
    async def on_msg(self, msg):
        pass

    async def on_start(self):
        async def on_message(message: AbstractIncomingMessage) -> None:
            async with message.process():
                await self.on_msg(message.body)
                # print(f"[x] {message.body!r}")

        connection = await connect(self.m_szUrl)

        async with connection:
            # Creating a channel
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            logs_exchange = await channel.declare_exchange(
                self.m_szQueue, ExchangeType.FANOUT,
            )

            # Declaring queue
            queue = await channel.declare_queue(exclusive=True)

            # Binding the queue to the exchange
            await queue.bind(logs_exchange)

            # Start listening the queue
            await queue.consume(on_message)

            # print(" [*] Waiting for logs. To exit press CTRL+C")
            await asyncio.Future()
