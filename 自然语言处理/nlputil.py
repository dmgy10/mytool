# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:46:08 2019

@author: yuyh2
"""
import pandas as pd
import numpy as np
import re

class NLPPreprocess:
    """
    word-id转换
    @param: obj: type:list
    @param: type:=0:word-id, =1:id-word
    @return: type:DataFrame
    """
    @staticmethod
    def word2id(obj, tp = 0):
        obj = np.unique(obj)
        len_o = len(obj) + 1
        id_ = np.arange(1, len_o, 1)
        if tp == 0:
            result = pd.DataFrame({'id':id_}, index = obj)
        if tp == 1:
            result = pd.DataFrame({'word':obj}, index = id_)
        return result
    
    """
    标注
    @param: obj,需要标注的主体,type:str
    @Param: el,需要标注的部分, type:str
    @ctl: 需要如何标注,type:list,第一个元素为未匹配的标注,第二个元素为匹配的标注
    @se: 是否需要标注开始和结束位置,默认None不标注,可以设置[start, end], 例['s', 'e']
    @return: type:list
    """
    @staticmethod
    def wordtag(obj, el, ctl = ['N', 'Y'], se = None):
        obj_li = list(obj)
        tag = [ctl[0]]*len(obj_li)
        
        #匹配
        match_idx = re.finditer(el, obj)
        for i in match_idx:
            tag[i.start():i.end()] = [ctl[1]]*(i.end() - i.start())
            if se != None:
                tag[i.start()] = se[0]
                tag[i.end() - 1] = se[1]
        return tag
    
    """
    文本-词典映射
    @param: con:需要映射的文本或者list,type:str/list
    @param: dic:映射字典
    @return: list
    """
    @staticmethod
    def dic_map(con, dic):
        #con 可以是str/list, 如果是str,则转换为list
        if isinstance(con, str):
            con = list(con)
        
        #dic 判断dic类型,必须为dict,否则返回原数据
        if not isinstance(dic, dict):
            print('词典类型错误')
            return con
        def char_map(i):
            return dic[i]
        map_result = list(map(char_map, con))
        return map_result
    
if __name__ == '__main__':
    NLPPreprocess.wordtag('我们的故事是如此美丽', '美丽', se = ['start', 'end'])
    
    y = ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'Y']
    NLPPreprocess.word2id(y, type = 1)

    
    