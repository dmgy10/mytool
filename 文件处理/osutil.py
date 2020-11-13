# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:15:18 2019

@author: yuyh2
"""

"""
工业大脑数据筛选
"""


import os

class OsUtil:
    """
    @param: file_dir,目录
    @return: type:dict,键: root: 根目录 dirs:目录下面的所以子目录 files: 当前目录下的所有文件名
    """
    @staticmethod
    def file_name(file_dir):
        result = {}
        result['root'] = []
        result['dirs'] = []
        result['files'] = []
        for root, dirs, files in os.walk(file_dir):
            result['root'].append(root)
            result['dirs'].append(dirs)
            result['files'].append(files)
        return result
        

if __name__ == '__main__':   
    result = OsUtil.file_name(r'E:\工作\数据挖掘项目\品类分类\p - 品类分类\data\小类_13594')
    result.get('files')
    result.get('root')