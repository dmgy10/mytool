# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:04:39 2019

@author: yuyh2
"""


import dbtool
import log
import time

#连接数据库
host = '10.17.158.73'
port = 3306
user = 'root'
password = '123456'
database = 'db_meicloud_ibrain_platform_wuxi_uat'
dao = dbtool.Dao(host, port, user, password, database)

#初始化log
log_ = log.Log(file_name = 'D:\\Users\\YUYH2\\Desktop\\log', table_name = 'logging_test')

#test_1:将日志输出写在方法内
def get_data(mode = 'mysql'):
    time_s = log_.get_recent_time()
    try:
        print('this is right')
        is_success = log_.SUC
        exception = None
    except Exception as e:
        exception = str(e)
        is_success = log_.FAI
    time_e = log_.get_recent_time()
    time_i = log_.get_spend_time(time_s, time_e)
    data_log = log_.get_log_data('get_data', is_success, time_i, exception)
    if mode == 'mysql':    
        dao.insert_data(data_log, log_.table_name)
    if mode == 'local':
        log_.write_log_to_local(data_log)
 
get_data()
    
#test_2：
def test_for(n):
    for i in range(n):
        time.sleep(1)
        print('error' + i)

def test_for_2(n, word = 'true', list_ = [1, 2, 1]):
    for i in range(n):
        time.sleep(1)
        print(word + str(i))
        print(list_)
        
def test_function(func_name, args, mode = 'mysql'):
    #构造可执行函数语句
    args_str = ''
    for i in args:
        if type(i) == str:
            args_str = args_str + '"' + i + '"' + ','
        else:
            args_str = args_str + str(i) + ','
    args_complete = func_name + '(' + args_str[:-1] + ')'
    
    time_s = log_.get_recent_time()
    try:
        eval(args_complete)
        is_success = log_.SUC
        exception = None
    except Exception as e:
        is_success = log_.FAI
        exception = str(e)
    time_e = log_.get_recent_time()
    time_i = log_.get_spend_time(time_s, time_e)
    data_log = log_.get_log_data(func_name, is_success, time_i, exception)
    if mode == 'mysql':    
        dao.insert_data(data_log, log_.table_name)
    if mode == 'local':
        log_.write_log_to_local(data_log)
 
test_function('test_for', [10],  mode = 'mysql')
test_function('test_for_2', [10, 'r', [1, 2]],  mode = 'local')