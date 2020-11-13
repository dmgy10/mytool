# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 17:01:53 2019

@author: yuyh2
"""

import numpy as np
import pandas as pd

class ListUtil:
    """
    将列表铺平
    @param:obj,类型：list
    @return:类型list
    """
    @staticmethod
    def list_flatten(obj):
        result = []
        for i in obj:
            if isinstance(i, list):
                result.extend(ListUtil.list_flatten(i))
            else:
                result.append(i)
        return result
    
    """
    删除列表中所有指定元素
    @param:obj,类型:list
    @param:el,类型可以为list/单个元素,需要删除的元素
    @return:类型:list
    """
    @staticmethod
    def list_remove_el(obj, el):
        result = None
        try:
            if isinstance(el, list):
                result = [i for i in obj if i not in el]
            else:
                result = [i for i in obj if i != el]
        except:
            print('数据类型error')
        return result
    
    """
    对列表元素计数
    @param:obj,类型:list
    @return:类型:DataFarme
    """
    @staticmethod
    def list_count(obj):
        unique = np.unique(obj, return_counts = True)
        result = pd.DataFrame({'value':list(unique[0]), 'counts':list(unique[1])})
        result = result.sort_values(by = 'counts', ascending = False)
        return result
    
    """
    判断两个列表的元素是否有交集、是否有完全相同的元素
    @param:list_1、list_2,类型:list
    @param: compare_type, =0 表示列表是否存在交集, =1 表示列表元素完全相同
    @return:类型:bool
    """
    @staticmethod
    def list_compare(list_1, list_2, compare_type = 0):
        if compare_type == 0:
            temp = np.intersect1d(list_1, list_2)
            temp_len = len(temp)
            if temp_len == 0:
                return False
            else:
                return True
        elif compare_type == 1:
            if len(list_1) != len(list_2):
                return False
            #先判断 list_1的元素是否全部在list_2中
            result_1 = []
            result_2 = []
            for i in list_1:
                if i in list_2:
                    result_1.append(True)
                else:
                    result_1.append(False)
            for i in list_2:
                if i in list_1:
                    result_2.append(True)
                else:
                    result_2.append(False)
            if all(result_1) and all(result_2):
                return True
            else:
                return False
        else:
            print('参数错误')
            return list_1
    
    """
    判断两个列表的逻辑值是否都是True
    @Param:list
    @param:type:list
    @param:how all:两个值都为True则返回True, any:任意一个为True则返回True
    @return:type:list 值为逻辑值
    """
    @staticmethod
    def list_true(list_1, list_2, how = 'all'):
        if len(list_1) != len(list_2):
            print('参数不符合要求')
            return 0
        result = []
        if how == 'all':
            for i in range(len(list_1)):
                if list_1[i] and list_2[i]:
                    result.append(True)
                else:
                    result.append(False)
        if how == 'any':
            for i in range(len(list_1)):
                if list_1[i] or list_2[i]:
                    result.append(True)
                else:
                    result.append(False)
        return result
                
class DFUtil:
    """
    单个变量筛选-完全等于哪些关键词
    @param: data,type:DataFrame
    @param: ctl:需要筛选的列及筛选内容,type:dict
    @return: data,type:DataFrame
    """
    @staticmethod
    def filter_f(data, ctl = {}):
        len_ctl = len(ctl)
        if len_ctl == 0:
            return data
        else:
            for key,value in ctl.items():
                data = data[data[key].isin(value)]
            return data
    """
    将数据框转化为dict
    @param: df:type:DataFrame
    @param: tp:0为索引为键, 1为列为键
    @return: type:dict
    """
    @staticmethod
    def df_dic(df, tp = 1):
        if tp == 0:
            len_df = df.T.shape[0]
            result = df.T.to_dict('list')
            if len_df == 1:
                for i in result:
                    result[i] = result[i][0]
        if tp == 1:
            len_df = df.shape[0]
            result = df.to_dict('list')
            if len_df == 1:
                for i in result:
                    result[i] = result[i][0]
        return result
        
        

if __name__ == '__mian__':
    x = [1, 2, [3, [4, 5]], 1, 1]
    ListUtil.list_count([1, 1, 2, 2, 3])
    
    data = pd.DataFrame({'A':['li', 'li', 'li', 'ta', 'ta'], 'B':['a', 'a', 'b', 'b', 'b']})
    DFUtil.filter_f(data, {'A':['li'], 'B':['a']})
    
    
    

    