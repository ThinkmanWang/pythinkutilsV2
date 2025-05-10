# -*- coding: UTF-8 -*-

import sys
import os
import asyncio

from abc import *
from aiokafka import AIOKafkaConsumer
from pythinkutils.common.datetime_utils import *
from pythinkutils.aio.common.aiolog import g_aio_logger
from pythinkutils.config.Config import g_config

class ThinkAioKafkaConsumer(object):
    __metaclass__ = ABCMeta

    def __init__(self
                 , szHost
                 , szTopic
                 , szGroup
                 , timeout_ms=0
                 , max_records=1024
                 , checkpoint_interval=10):
        self.m_szHost = szHost
        self.m_szTopic = szTopic
        self.m_szGroup = szGroup
        self.m_bStarted = False

        if timeout_ms <= 10:
            timeout_ms = 10
        self.m_nTimeout = timeout_ms
        self.m_nMaxRecords = max_records
        self.m_nCheckpointInterval = checkpoint_interval
        self.m_nLastCheckpoint = 0

    def start(self):
        if self.m_bStarted:
            return

        asyncio.gather(self.on_start())

        self.m_bStarted = True

    @abstractmethod
    async def on_msg(self, msg):
        pass

    @abstractmethod
    async def on_checkpoint(self):
        pass

    async def on_start(self):
        while True:
            g_aio_logger.info("Start Kafka consumer")
            consumer = AIOKafkaConsumer(self.m_szTopic
                                        , loop=asyncio.get_event_loop()
                                        , bootstrap_servers=self.m_szHost
                                        , group_id=self.m_szGroup
                                        , auto_commit_interval_ms=1000
                                        , auto_offset_reset="earliest")

            try:
                await consumer.start()

                while True:
                    result = await consumer.getmany(timeout_ms=self.m_nTimeout, max_records=self.m_nMaxRecords)
                    for tp, messages in result.items():
                        if messages:
                            lstTask = []
                            for msg in messages:
                                task = asyncio.create_task(self.on_msg(msg))
                                lstTask.append(task)

                            for task in lstTask:
                                await task

                            await consumer.commit({tp: messages[-1].offset + 1})
                        else:
                            await asyncio.sleep(1)

                    if get_timestamp() - self.m_nLastCheckpoint > self.m_nCheckpointInterval:
                        self.m_nLastCheckpoint = get_timestamp()
                        await self.on_checkpoint()

                # Consume messages
                # async for msg in consumer:
                #     await self.on_msg(msg)
            except Exception as e:
                await g_aio_logger.error(e)
                await asyncio.sleep(1)
            finally:
                try:
                    await consumer.stop()
                except Exception as ex:
                    pass

