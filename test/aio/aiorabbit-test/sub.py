# -*- coding: utf-8 -*-

import asyncio

from pythinkutils.aio.rabbitmq.ThinkRabbitMQSub import ThinkRabbitMQSub

class MyConsumer(ThinkRabbitMQSub):
    async def on_msg(self, msg):
        print(msg)

def main():
    loop = asyncio.get_event_loop()

    myConsumer = MyConsumer("amqp://admin:123456@10.0.0.37/", "fxxk")
    myConsumer.start()

    loop.run_forever()

if __name__ == '__main__':
    main()
