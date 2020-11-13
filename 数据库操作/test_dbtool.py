# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:31:08 2019

@author: yuyh2
"""

from dbtool import Dao
import pandas as pd

#test0:初始化
d = Dao()

#test1:连接mysql
con = d.connet_to_mysql()

#test2:查询数据

#查全表
data_query_1 = d.query_data(table_name = 't_sa_keyword_train_source')

#查指定字段
data_query = d.query_data(table_name = 't_sa_keyword_train_source', columns = ['index_third', 'key_word'])

#test3:更新数据
sql = 'update test_name set name = "test" where name = "x"'
d.update_data(sql)

#test4:删除数据
sql = 'delete from test_dbtool where name = "lisa"'

#删除全表
d.delete_data(table_name = 'test_dbtool')

#删除指定sql语句
d.delete_data(sql = sql)

#test5:写入数据
data = pd.DataFrame({'id':[10, 11], 'name':['shiney', 'craig']})
d.insert_data(data, 'test_dbtool')

#test6:读取本地数据
#读取txt
data_txt = d.get_local_data('D:\\MyData\\yuyh2\\Desktop\\test_6.txt')
data_txt

#读取csv
#读取excel
data_xlsx = d.get_local_data('D:\\MyData\\yuyh2\\Desktop\\test_6.xlsx')
data_xlsx = d.get_local_data('D:\\MyData\\yuyh2\\Desktop\\test_6.xlsx', sheet = 'test')

#test7:写入数据到本地
data = pd.DataFrame({'A':[1, 2, 3], 'B':[4, 5, 7]})
data_2 = pd.DataFrame({'A':[11, 21, 31], 'B':[41, 51, 71]})
d.write_to_local('D:\\MyData\\yuyh2\\Desktop\\test_7.xlsx', data, sheets = 'z')
d.write_to_local('D:\\MyData\\yuyh2\\Desktop\\test_7.csv', data)
d.write_to_local('D:\\MyData\\yuyh2\\Desktop\\test_7.txt', data)
d.write_to_local('D:\\MyData\\yuyh2\\Desktop\\test_7.xlsx', [data, data_2], sheets = ['z1', 'z2'])
