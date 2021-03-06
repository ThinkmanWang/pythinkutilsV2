# -*- coding: UTF-8 -*-

import sys
import os
from typing import Optional, Any

import pymysql as mysql
import threading
from dbutils.pooled_db import PooledDB

from pythinkutils.config.Config import ThinkConfig

class ThinkMysql:
    g_lock = threading.Lock()
    g_dictConnPool = {}

    @classmethod
    def get_conn_pool_ex(cls, szGroup="mysql"):
        return cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                      , port=int(ThinkConfig.get_default_config().get(szGroup, "port"))
                      , user=ThinkConfig.get_default_config().get(szGroup, "user")
                      , password=ThinkConfig.get_default_config().get(szGroup, "password")
                      , db=ThinkConfig.get_default_config().get(szGroup, "db")
                      , mincached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections") / 2)
                      , maxcached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get(szGroup, "maxconnections"))
                      , charset="utf8"
                      , use_unicode=True)

    @classmethod
    def get_conn_pool(cls
                      , host=ThinkConfig.get_default_config().get("mysql", "host")
                      , port=int(ThinkConfig.get_default_config().get("mysql", "port"))
                      , user=ThinkConfig.get_default_config().get("mysql", "user")
                      , password=ThinkConfig.get_default_config().get("mysql", "password")
                      , db=ThinkConfig.get_default_config().get("mysql", "db")
                      , mincached = int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections") / 2)
                      , maxcached = int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get("mysql", "maxconnections"))
                      , charset = "utf8"
                      , use_unicode = True):

        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            with cls.g_lock:
                if cls.g_dictConnPool.get(szHostPortDb) is None:

                    conn_pool = PooledDB(mysql
                                         , mincached = mincached
                                         , maxcached = maxcached
                                         , host=host
                                         , user=user
                                         , password=password
                                         , db=db
                                         , port=port
                                         , maxconnections=maxconnections
                                         , charset = charset
                                         , use_unicode = use_unicode)

                    cls.g_dictConnPool[szHostPortDb] = conn_pool


        return cls.g_dictConnPool.get(szHostPortDb)

    @classmethod
    def query(cls, conn, szSql, args=None) -> Optional[list]:
        c = conn.cursor(mysql.cursors.DictCursor)
        c.execute(szSql, args)
        rows = c.fetchall()

        return rows

    @classmethod
    def execute(cls, conn, szSql, args=None, bAutoCommit=True) -> int:
        cur = conn.cursor(mysql.cursors.DictCursor)

        nRet = cur.execute(szSql, args)

        if bAutoCommit:
            conn.commit()

        return nRet

    @classmethod
    def get_last_insert_id(cls, conn) -> int:
        try:
            lstRows = cls.query(conn, "SELECT LAST_INSERT_ID() as id")
            if lstRows is None or len(lstRows) <= 0:
                return 0

            return lstRows[0]["id"]
        except Exception as ex:
            return 0

    @classmethod
    def get_all_tables(cls, conn):
        lstRet = []

        c = conn.cursor()
        try:
            c.execute('''
                show tables
            ''')
            rows = c.fetchall()

            for row in rows:
                lstRet.append(row[0])

        except Exception as e:
            pass
        finally:
            return lstRet

    @classmethod
    def get_table_detail(cls, conn, szTable) -> list:
        lstRow = cls.query(conn, "SHOW FULL COLUMNS FROM {}".format(szTable))
        return lstRow