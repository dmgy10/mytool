# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:15:50 2019

@author: yuyh2
"""

import re

class PyStr:
    """
    去掉所有的空格符号
    @param:stri:可以是单个str，可以是list的str
    @return:单个str或者list
    """
    @staticmethod
    def str_remove_blank_all(stri):
        try:
            if isinstance(stri, str):
                str_n = re.sub(' +', '', stri)
                return str_n
            if isinstance(stri, list):
                str_n = []
                for i in stri:
                    str_t = re.sub(' +', '', i)
                    str_n.append(str_t)
                return str_n
        except:
            print('格式不正确')
            return stri
    """
    去掉中间的多余空格符号
    @param:stri:可以是单个str，可以是list的str
    @return:单个str或者list
    """
    @staticmethod
    def str_remove_balnk_extra(stri):
        try:
            if isinstance(stri, str):
                stri = stri.strip()
                str_n = re.sub(' +', ' ', stri)
                return str_n
            if isinstance(stri, list):
                str_n = []
                for i in stri:
                    i = i.strip()
                    str_t = re.sub(' +', ' ', i)
                    str_n.append(str_t)
                return str_n
        except:
            print('格式不正确')
            return stri
        
    """
    判断多个词是否包含在一个字符串内
    @param:type: str
    @param:el:list,需要判断是否包含的list
    """
    @staticmethod
    def str_contain(obj, el, how = 'all'):
        l = []
        for i in el:
            temp = i in obj
            l.append(temp)
        if how == 'all':
            return all(l)
        elif how == 'any':
            return any(l)
        else:
            print('参数错误')
            return 0
    """
    判断一个字符串内同时包含某些词 同时不包含某些词
    @param:obj type: str
    @param:con:list,需要判断是否包含的list
    @param:notcon:list 不包含的词
    @return: type:list 
    """
    @staticmethod
    def str_multi_contain(obj, con = [], notcon = []):
        def is_true(list_1, list_2):
            result = []
            for i in range(len(list_1)):
                if list_1[i] and list_2[i]:
                    result.append(True)
                else:
                    result.append(False)
            return result
        
        #同时包含
        list_con = [PyStr.str_contain(i, con) for i in obj]
        
        #同时不包含
        p_notcon = '|'.join(notcon)
        list_notcon = ReUtil.re_defect(obj, p_notcon, reverse = True)
        list_result = is_true(list_con, list_notcon)
        return list_result
            
        
class ReUtil:   
    """
    批量执行re的匹配1-提取
    """
    @staticmethod
    def re_findall(obj, pattern):
        map_list = list(map(lambda x:re.findall(pattern, x), obj))
        return map_list
    
    """
    批量执行re的匹配1-判断是否匹配
    """
    @staticmethod
    def re_defect(obj, pattern):
        def defect(x):
            if re.search(pattern, x):
                return True
            else:
                return False
        map_list = list(map(defect, obj))
        return map_list
    
    """
    批量执行re的匹配1-匹配位置
    """
    @staticmethod
    def re_loc(obj, pattern):
        def loc(x):
            loc_list = []
            temp = re.finditer(pattern, x)
            for i in temp:
                tem_f = []
                tem_f.append(i.start())
                tem_f.append(i.end())
                loc_list.append(tem_f)
            return loc_list
        map_list = list(map(loc, obj))
        return map_list
    
    """
    批量执行re的匹配1-替换
    """
    @staticmethod
    def re_sub(obj, pattern, sub):
        def sub_func(x):
            temp = re.sub(pattern, sub, x)
            return temp
        map_list = list(map(sub_func, obj))
        return map_list
    
    """
    批量执行re的匹配1-删除
    """
    @staticmethod
    def re_remove(obj, pattern):
        def sub_func(x):
            temp = re.sub(pattern, '', x)
            return temp
        map_list = list(map(sub_func, obj))
        return map_list
    
    
if __name__ == '__main__':
    x = ['  jbl   akg   ', 'this   is my  ']
    PyStr.str_remove_balnk_extra(x) #1
    PyStr.str_remove_blank_all(x) #2
    
    
    
    
    
                
            
    
    
        
        
        
        