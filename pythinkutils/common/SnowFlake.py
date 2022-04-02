# -*- coding: utf-8 -*-

import time
import datetime

class ThinkSnowFlake(object):
    # twitter's snowflake parameters
    _twepoch = 1288834974657
    _datacenter_id_bits = 5
    _worker_id_bits = 5
    _sequence_id_bits = 12
    _max_datacenter_id = 1 << _datacenter_id_bits
    _max_worker_id = 1 << _worker_id_bits
    _max_sequence_id = 1 << _sequence_id_bits
    _max_timestamp = 1 << (64 - _datacenter_id_bits - _worker_id_bits - _sequence_id_bits)

    @classmethod
    def _make_snowflake(cls, timestamp_ms, datacenter_id, worker_id, sequence_id, twepoch=_twepoch):
        """generate a twitter-snowflake id, based on
        https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
        :param: timestamp_ms time since UNIX epoch in milliseconds"""

        sid = ((
                           int(timestamp_ms) - twepoch) % cls._max_timestamp) << cls._datacenter_id_bits << cls._worker_id_bits << cls._sequence_id_bits
        sid += (datacenter_id % cls._max_datacenter_id) << cls._worker_id_bits << cls._sequence_id_bits
        sid += (worker_id % cls._max_worker_id) << cls._sequence_id_bits
        sid += sequence_id % cls._max_sequence_id

        return sid

    @classmethod
    def _melt(cls, snowflake_id, twepoch=_twepoch):
        """inversely transform a snowflake id back to its parts."""
        sequence_id = snowflake_id & (cls._max_sequence_id - 1)
        worker_id = (snowflake_id >> cls._sequence_id_bits) & (cls._max_worker_id - 1)
        datacenter_id = (snowflake_id >> cls._sequence_id_bits >> cls._worker_id_bits) & (cls._max_datacenter_id - 1)
        timestamp_ms = snowflake_id >> cls._sequence_id_bits >> cls._worker_id_bits >> cls._datacenter_id_bits
        timestamp_ms += twepoch

        return (timestamp_ms, int(datacenter_id), int(worker_id), int(sequence_id))

    @classmethod
    def _local_datetime(cls, timestamp_ms):
        """convert millisecond timestamp to local datetime object."""
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000.)

    @classmethod
    def id(cls):
        time.sleep(0.01)
        t0 = int(time.time() * 1000)
        return cls._make_snowflake(t0, 0, 0, 0)