# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:15:15 2019

@author: YUYH2
"""

import pymysql
import pandas as pd
import re
from sqlalchemy import create_engine

'''
连接mysql数据源
'''

class Dao:
    def __init__(self,host='10.16.26.215',port = 3306,user = 'datamining',password = 'Nr2AFk4o',database = 'db_gxt_datamining_common'):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    """
    连接数据库
    """
    def connet_to_mysql(self):
        conn = pymysql.connect(host = self.host, port = self.port, user = self.user, password = self.password, database = self.database)
        return conn
    
    """
    查询数据
    返回DataFrame
    :param category_name:要查询的品类名称，如果为空，则查询全表
    :param table_name:要查询的表，如果此参数为空，则自定义查询
    :param sql:查询的sql，如果此参数不为*，则查询获取指定指定字段
    """
    def query_data(self, sql = '*', table_name = None, category_name = None):
        #连接数据库
        conn = self.connet_to_mysql()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        data = None
        # 常规查询，设置获取字段名称、表名和品类名
        if table_name != None and category_name == None:  
            sql = 'select {sql} from {table_name} '.format(sql=sql,table_name = table_name)
        elif table_name != None and category_name != None:
            sql = "select "+sql+" from "+table_name+" where category_name=" + "'" + category_name + "'"
        #查询全量数据
        #if sql is None and table_name is not None:
        #    sql = 'select * from {table_name} '.format(table_name = table_name)
        #自定义sql查询数据
        elif table_name == None:
            sql = sql
        else:
            print('参数错误')
            return data
        cursor.execute(sql)
        data_source = cursor.fetchall()
        
        #将数据转成数据框
        try:
            data = pd.DataFrame(data_source)
        except Exception as e:
            print('数据为空:', str(e))
            return data
        conn.close()
        return data
    
    """
    更新数据
    """
    def update_data(self, sql):
        #连接数据库
        conn = self.connet_to_mysql()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    
    """
    删除数据
    """
    def delete_data(self, table_name = None, sql = None):
        conn = self.connet_to_mysql()
        cursor = conn.cursor()
        if table_name is None and sql is not None:
            sql = sql
        elif table_name is not None and sql is None:
            sql = 'delete from {table_name}'.format(table_name = table_name)
        else:
            print('参数错误')
            return
        cursor.execute(sql)
        conn.commit()
        conn.close()
        
    """
    写入数据
    """
    def insert_data(self, data, table_name):
        try:
            engine = create_engine('mysql+pymysql://' + self.user + ':' + str(self.password) + '@' + str(self.host) + ':' + str(self.port) +  '/' + self.database + '?charset=utf8')
            data.to_sql(table_name, engine, if_exists='append', index = False)
        except Exception as e:
            print(str(e))
            print(table_name,'写入数据失败')
    

    """
    获取本地数据
    :file:为文件路径及文件名，目前支持.xlsx .csv .txt
    """
    @staticmethod
    def get_local_data(file, sheet = None):
        data = None
        try:
            if re.search('\.xlsx?$', file):
                if sheet is not None:
                    data = pd.read_excel(file, sheet = sheet)
                else:
                    data = pd.read_excel(file)
            elif re.search('\.csv$', file):
                data = pd.read_csv(file)
            elif re.search('\.txt', file):
                data = pd.read_table(file)
            else:
                print('参数错误：不支持的文件')
        except Exception as e:
            print('读取文件错误')
        return data
    
    """
    写入本地,支持结构化的数据(DataFrame), 写入csv、xlsx
    """
    @staticmethod
    def write_to_local(file, data):
        try:
            if re.search('\.xlsx?$', file):
                data.to_excel(file)
            elif re.search('\.csv$', file):
                data.to_csv(file)
            #elif re.search('\.txt', file):
            #   with open(file, 'w') as f:
            #       f.write(data)
        except:
            print('写入数据失败')