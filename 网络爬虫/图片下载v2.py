# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:35:30 2019

@author: yuyh2
"""

from urllib.request import urlretrieve
import os
import pandas as pd

#链接处理
def url_modify(data):
    url_new = []
    for i in data:
        try:
            if 'http' not in i:
                i = 'http:' + str(i)
        except:
            i = i
        url_new.append(i)
    return url_new

#图片下载 
def urllib_image_download(image_url, image_dir, image_name):
    download_dir = os.path.join('./', image_dir)
    os.makedirs(download_dir, exist_ok = True)
    urlretrieve(image_url, os.path.join(download_dir, image_name + '.png'))

#淘系   
def url_download(data, by = 'item_cat_id'):
    data = data.reset_index(drop = True)
    size = data.shape[0]
    for i in range(size):
        temp = data.iloc[i, :]
        try:
            urllib_image_download(temp['img_url'], by + '_' + str(temp[by]), 'P_' + str(temp['item_id']) + '_' + str(temp['month_sale']))
        except:
            print('下载错误: ' + str(temp['img_url']))
            pass
        
#京东
def url_download_jd(data, by = 'item_cat_id'):
    data = data.reset_index(drop = True)
    size = data.shape[0]
    for i in range(size):
        temp = data.iloc[i, :]
        try:
            urllib_image_download(temp['img_url'], by + '_' + str(temp[by]), 'P_' + str(temp['item_id']) + '_' + str(temp['total_comment']))
        except:
            print('下载错误: ' + str(temp['img_url']))
            pass

#淘系图片下载
def download_pc_tb(data, n):
    #淘系
    data_test = data.sort_values('month_sale', ascending = False)
    data_1 = data_test[data_test['platform_name'] != '京东'].iloc[:n, :]

    #图片下载
    data_1['img_url'] = url_modify(data_1['img_url']) #链接处理
    url_download(data_1, by = 'item_cat_id')

#京东图片下载
def download_pc_jd(data, n):
    #京东
    data_test = data.sort_values('total_comment', ascending = False)
    data_2 = data_test[data_test['platform_name'] == '京东'].iloc[:n, :]

    #图片下载
    data_2['img_url'] = url_modify(data_2['img_url']) #链接处理
    url_download_jd(data_2, by = 'item_cat_id')
    

    
    
if __name__ == '__main__':
    #下载测试
    os.chdir(r'D:\MyData\yuyh2\Desktop\bs')
   
    #step1：数据读取
    data_test = pd.read_csv(r'basketball.csv', engine = 'python')
    
    #淘系
    download_pc_tb(data_test, 10)   #10为销量前10的图片   
    
    #京东
    download_pc_jd(data_test, 10) # 10为评论量前10的图片
    