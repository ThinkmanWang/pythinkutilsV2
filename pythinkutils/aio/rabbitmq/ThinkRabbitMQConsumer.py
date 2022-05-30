# -*- coding: utf-8 -*-

import asyncio
import aio_pika
import aio_pika.abc
from abc import *

class ThinkRabbitMQConsumer(object):
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
        connection = await aio_pika.connect_robust(
            self.m_szUrl, loop=asyncio.get_event_loop()
        )

        async with connection:
            # Creating channel
            channel: aio_pika.abc.AbstractChannel = await connection.channel()

            # Declaring queue
            queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
                self.m_szQueue
                , auto_delete=False
                , durable=True
            )

            async with queue.iterator() as queue_iter:
                # Cancel consuming after __aexit__
                async for message in queue_iter:
                    async with message.process():
                        # print(message.body)
                        await self.on_msg(message.body)

                        # if queue.name in message.body.decode():
                        #     break