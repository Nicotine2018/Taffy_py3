# coding=utf-8
import sys
import os
#import pymssql

from Util.DBTool.baseUtil import *


class SqlserverUtil(BaseUtil):
    """数据库工具类，提供连接池以及执行sql语句的方法"""

    def __init__(self, connection):
        """Constructor"""
        super(SqlserverUtil, self).__init__(connection)
        self.cursor = self.connection.cursor()

    def executeQuery(self, sql, params=()):
        data = []
        result = self.cursor.execute(sql, params)
        data = self.cursor.fetchall()

        for row in data:
            if isinstance(row, dict):
                for key in row:
                    if isinstance(row[key], bytes):
                        try:
                            row[key] = row[key].decode('iso8859-1').encode('gbk')
                        except UnicodeError:
                            pass
        return data

    def executeNonQuery(self, sql, params=()):
        try:
            result = 0
            self.cursor.execute(sql, params)
            self.connection.commit()
            result = self.cursor.rowcount
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print (e)
        finally:
            return result
