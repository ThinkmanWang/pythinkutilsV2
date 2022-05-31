# -*- coding: utf-8 -*-

import asyncio

from pythinkutils.aio.rabbitmq.ThinkRabbitMQConsumer import ThinkRabbitMQConsumer
from pythinkutils.config.Config import g_config

class MyConsumer(ThinkRabbitMQConsumer):
    async def on_msg(self, msg):
        print(msg)

def main():
    loop = asyncio.get_event_loop()

    myConsumer = MyConsumer(g_config.get("rabbitmq", "url"), g_config.get("rabbitmq", "queue"))
    myConsumer.start()

    loop.run_forever()

if __name__ == '__main__':
    main()
