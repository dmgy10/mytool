# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 16:46:44 2019

@author: yuyh2
"""
import jieba

class Wordcut:
    """
    将所有列表都铺平
    """
    @staticmethod
    def flatten_list(obj):
        result = []
        for i in obj:
            if isinstance(i, str):
                result.append(i)
            if isinstance(i, list):
                result.extend(Wordcut.flatten_list(i))
        return result
            
    """
    分词
    :param: word 待分词的语句，类型: str/list
    :param: platten:是否将列表铺平
    """
    @staticmethod
    def word_cut(word, flatten = False):  # 只有字符串形式才可以分词
        if isinstance(word, str):
            return jieba.lcut(word)
        else:
            word_list = []
            for i in word:
                if isinstance(i, str):
                    word_list.append(jieba.lcut(i))
            if flatten:
                word_list = Wordcut.flatten_list(word_list)
            return word_list
    
    """
    运用停止词  
    """
    @staticmethod
    def remove_stop_words(word, stop_words):
        result = []
        for i in word:
            if isinstance(i, list):
                result.extend(Wordcut.remove_stop_words(i, stop_words))
            if isinstance(i, str):
                if i not in stop_words:
                    result.append(i)
        return result
    
if __name__ == '__main__':
    word =  ['这是', '很好', '的']
    stop_words = ['的', '呢']
    w = Wordcut()
    w.word_cut(['这里的', '风景很好'], flatten = True)
    w.remove_stop_words([word, word], stop_words)       
            
        