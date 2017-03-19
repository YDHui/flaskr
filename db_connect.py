#coding:utf8
import MySQLdb
import MySQLdb.cursors
from MySQLdb import ProgrammingError
import time
import logging

class MysqlOprate:
    """
        mysql 操作类
        初始化参数：
            DB = MysqlOprate(dbhost,dbuser,dbpass,dbport,charset)
            charset 是可选参数，默认是utf8
        data_query 方法是数据查询 方法，即 select 语句
        dml_exec  方法是 dml  insert,delete,update,  成功返回0，失败返回1
        conn_close  方法  关闭数据库连接，每次执行完data_query、dml_exec后，记得执行此方法
    """
    def __init__(self,db_ip,db_user,db_pass,db_port,charset='utf8'):
        self.logger = logging.getLogger('scripts')
        self.DBHOST = db_ip
        self.DBUSER = db_user
        self.DBPWD = db_pass
        self.DBPORT = db_port
        self.CHARSET = charset
        try:
            self.conn = MySQLdb.connect(host = self.DBHOST, user = self.DBUSER,
                                         passwd = self.DBPWD,port = self.DBPORT,charset = self.CHARSET)
        except Exception,e:
            self.logger.info(e)

    def data_query(self,sql):
        '''
            data query
            return: ({key:value},{},{}...)
        '''
        try:
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception,error:
            return {'error':error.args}

    def dml_exec(self,sql):
        '''
            dml exec, insert,delete,update
            success, return 0  else return 1
        '''
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            _ret_code = 0
        except Exception,e:
            _ret_code = 1
        return _ret_code

    def conn_close(self):
        self.conn.close()

