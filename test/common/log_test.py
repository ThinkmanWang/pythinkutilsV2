# -*- coding: utf-8 -*-

from pythinkutils.common.log import g_logger

def main():
    g_logger.info("Hello World")
    g_logger.info("Hello %s" % ("FXXK", ))

if __name__ == '__main__':
    main()