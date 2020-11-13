# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:38:21 2019

@author: yuyh2
"""

import time
import pandas as pd
import logging
import datetime

class Log:
    #file_name为路径+文件名（不加后缀）例：'D:\\Users\\YUYH2\\Desktop\\log'
    def __init__(self, project = 'project00', class_name = 'class00', file_name = None, table_name = None):
        self.project = project
        self.class_name = class_name
        self.SUC = 'success'
        self.FAI = 'fail'
        self.file_name = file_name #写入数据库表名
        self.table_name = table_name #写入本地文件名
    
    """
    获取当前时间
    """
    def get_recent_time(self):
        time_s = time.time()
        return time_s
    
    """
    计算总耗时时间,mode = s(秒)/h(小时)
    """
    def get_spend_time(self, time_s, time_e, mode = 's'):
        time_interval = time_e - time_s
        if mode == 's':
            return round(time_interval, 2)
        if mode == 'h':
            return round(time_interval/(60*60), 2)
    
    """
    标准化日志内容
    """
    def get_log_data(self, method_name, is_success, time, exception):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = pd.DataFrame(columns = ['project', 'class', 'method', 'is_success', 'time', 'exception', 'created_time'])
        data = data.append({'project':self.project, 'class':self.class_name, 'method':method_name, 'is_success':is_success, 'time':time, 'exception':exception, 'created_time':now}, ignore_index = True)
        return data
    
    """
    将日志写入本地,日志名为：file日期.txt, 例log2019-09-17.txt
    """
    def write_log_to_local(self, data_log):
        #获取今天日期
        date = datetime.date.today().strftime('%Y-%m-%d')
        
        #设置日志输出
        logging.basicConfig(level = logging.DEBUG, filename = self.file_name + date + '.txt',
                    filemode='a',format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        
        #日志写入内容
        logging.info('project: ' + self.project)
        logging.info('class: ' + self.class_name)
        logging.info('method: ' + data_log['method'][0])
        logging.info('is_sucees: ' + data_log['is_success'][0])
        logging.info('time: ' + str(data_log['time'][0]))
        logging.info('exception: ' + str(data_log['exception'][0]))
        logging.info('\n\n')
        