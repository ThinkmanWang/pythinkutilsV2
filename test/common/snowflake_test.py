# -*- coding: utf-8 -*-

from pythinkutils.common.SnowFlake import ThinkSnowFlake
from pythinkutils.common.log import g_logger

def main():

    setId = set()
    for i in range(1000):
        nId = ThinkSnowFlake.id()
        g_logger.info(ThinkSnowFlake.id())
        setId.add(nId)

    g_logger.info(len(setId))

if __name__ == '__main__':
    main()
