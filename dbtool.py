# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:15:15 2019

@author: YUYH2
"""

import pymysql
from pyhive import hive
import pandas as pd
import re
from sqlalchemy import create_engine

'''
连接mysql数据源
'''

class Dao:
    def __init__(self, host='10.16.26.215',port = 3306,user = 'datamining',password = 'Nr2AFk4o',database = 'db_gxt_datamining_common'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    """
    连接mysql
    """
    def connet_to_mysql(self):
        conn = None
        try:
            conn = pymysql.connect(host = self.host, port = self.port, user = self.user, password = self.password, database = self.database)
        except Exception as e:
            print('mysql连接错误: ' + str(e))
        return conn
    
    """
    连接hive
    """
    def connect_to_hive(self):
        conn = None
        try:
            conn = hive.Connection(host = self.host, port = self.host, database = self.database, username = self.user)
        except Exception as e:
            print('hive连接错误: ' + str(e))
            return conn
        
    
    """
    查询数据:mysql
    返回DataFrame
    :param columns:类型[],需要查询的列
    :param table_name:要查询的表，如果此参数为空，则自定义查询
    :param sql:查询的sql，如果此参数不为*，则查询获取指定指定字段
    """
    def query_data(self, table_name = None, sql = None, columns = None):
        
        #连接数据库
        conn = self.connet_to_mysql()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        data = None
        
        # 查询全表数据
        if table_name != None and columns == None:  
            sql = 'select * from {table_name} '.format(sql=sql,table_name = table_name)
        
        #查询指定字段
        elif table_name != None and columns != None and isinstance(columns, list):
            col = ','.join(columns)
            sql = 'select {col} from {table_name}'.format(col = col, table_name = table_name)
        
        #自定义sql查询数据
        elif sql != None:
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
    查询数据:hive
    返回DataFrame
    :param columns:类型[],需要查询的列
    :param table_name:要查询的表，如果此参数为空，则自定义查询
    :param sql:查询的sql，如果此参数不为*，则查询获取指定指定字段
    """
    def query_data_hive(self, table_name = None, sql = None, columns = None):
        data = None
        
        #连接hive
        con = self.connect_to_hive()
        
        try:
            if table_name != None:
                sql = 'select * from {table_name}'.format(table_name = table_name)
            if sql != None:
                sql = sql
            elif table_name != None and columns != None and isinstance(columns, list):
                col = ','.join(columns)
                sql = 'select {col} from {table_name}'.format(col = col, table_name = table_name) 
            data = pd.read_sql(sql, con)
        except Exception as e:
            print('数据获取失败: ' + str(e))
        
        con.close()
        return data
    
    """
    更新数据
    :param sql:需要执行的sql语句
    """
    def update_data(self, sql):
        #连接数据库
        conn = self.connet_to_mysql()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        
    #通过字典更新表
    def update_data_dict(self,table_name,values_map,limit_map):

        try:
            conn = self.connet_to_mysql()
            cursor = conn.cursor()
            limit_keys = "=%s and ".join(limit_map.keys()) + '=%s'
            value_key = "=%s , ".join(values_map.keys()) + '=%s'
            all_values = list(values_map.values()) + list(limit_map.values())
            sql = "update {table_name} set %s where %s ".format(table_name=table_name) % (value_key, limit_keys)
            nums = cursor.execute(sql, all_values)
            conn.commit()
            conn.close()
            return nums
        except Exception as e:
            #logging.error(errorcode.Update_Sql_Error + ':' + str(e))
            raise e
    
    """
    删除数据
    支持两种删除操作，（1）删除全表；（2）执行sql语句删除
    :param table_name：表名，如果不为空，则删除全表
    :param sql:sql语句
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
    :param data:data,需要写入表的数据,类型DataFrame
    :param table_name:表名,需要写入表的表名
    """
    def insert_data(self, data, table_name):
        try:
            engine = create_engine('mysql+pymysql://' + self.user + ':' + str(self.password) + '@' + str(self.host) + ':' + str(self.port) +  '/' + self.database + '?charset=utf8')
            data.to_sql(table_name, engine, if_exists='append', index = False)
        except Exception as e:
            print(str(e))
            print(table_name,'写入数据失败')
    
    #根据字典插入数据(适用于单条数据)
    def insert_data_dict(self,table_name, values_map):

        try:
            keys = ", ".join(values_map.keys())
            qmark = ", ".join(["%s"] * len(values_map))
            sql = "insert into {table_name}(%s) values (%s)".format(table_name=table_name) % (keys, qmark)
            conn = self.connet_to_mysql()
            cursor = conn.cursor()
            nums = cursor.execute(sql, list(values_map.values()))
            conn.commit()
            conn.close()
            return nums
        except Exception as e:
            #logging.error(errorcode.Insert_Sql_Error + ':' + str(e))
            raise e
    

    """
    获取本地数据
    :file:为文件路径及文件名，目前支持.xlsx .csv .txt
    :sheet:sheet名，仅当读取excel生效
    """
    @staticmethod
    def get_local_data(file, sheet = None):
        data = None
        try:
            if re.search('\.xlsx?$', file):
                if sheet is not None:
                    data = pd.read_excel(file, sheetname = sheet)
                else:
                    data = pd.read_excel(file)
            elif re.search('\.csv$', file):
                data = pd.read_csv(file)
            elif re.search('\.txt', file):
                data = pd.read_table(file)
            else:
                print('参数错误：不支持的文件')
        except Exception as e:
            print('读取文件错误: ' + str(e))
        return data
    
    """
    写入本地,支持结构化的数据(DataFrame), 写入csv、xlsx、txt
    :data:需要写入表的数据,如果要写入多份数据到excel,类型需要为[],元素为DataFrame类型
    :sheets:sheet名，写入excel失效,如果是写入多份数据到excel, sheets需要为[]
    """
    @staticmethod
    def write_to_local(file, data, sheets = None):
        try:
            if re.search('\.xlsx?$', file) and not isinstance(data, list):
                data.to_excel(file, sheets)
            elif re.search('\.csv$', file) and not isinstance(data, list):
                data.to_csv(file)
            elif re.search('\.xlsx?$', file) and isinstance(data, list) and isinstance(sheets, list):
                writer = pd.ExcelWriter(file)
                for i in range(len(data)):
                    data[i].to_excel(writer, sheets[i])
                writer.save()
                writer.close()
            elif re.search('\.txt?$', file):
                with open(file, mode='w', encoding='utf-8') as f:
                    f.writelines(str(data))        
        except Exception as e:
            print('写入数据失败: ' + str(e))