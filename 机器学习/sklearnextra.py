# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:48:06 2019

@author: yuyh2
"""
import pandas as pd
from sklearn.tree import _tree
import pandas as pd

class Sample:
    """
    分层抽样
    """
    #对单个组抽样
    @staticmethod
    def sample_diy(data, frac):
        return data.sample(int(data.shape[0] * frac))
    
    #分组抽样
    @staticmethod
    def group_sample(data, label, frac):
        data_temp = data.groupby(by = [label]).apply(Sample.sample_diy, frac = frac)
        data_temp = data_temp.reset_index(drop = True)
        return data_temp
    
class TreeExtra:
    
    """
    特征重要性输出
    @param: model,训练好的模型
    @param: train_set, 训练数据
    @param: key_n: 选择最重要的k个特征,type:int
    @return: type:DataFrame
    """
    @staticmethod
    def tree_importance(model, train_set, key_n):
        importance = model.feature_importances_
        imp_df = pd.DataFrame({'word':train_set.columns, 'value':importance}).sort_values(by = 'value', ascending = False).reset_index(drop = True)
        imp_df_filter = imp_df.loc[:key_n - 1,:]
        return imp_df_filter
    
    """
    决策树原始规则输出
    @param: tree:训练好的模型
    @param: feature_name:特征名称
    @return: type:list
    """
    @staticmethod
    def tree_to_code(tree, feature_names):
        print('输出规则: ')
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        pathto=dict()
        
        global k
        k = 0
        
        #规则存档
        rule_all = []
        def recurse(node, depth, parent):
            global k
            #indent = "  " * depth
            
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                s= "{} <= {} ".format( name, threshold, node )
                if node == 0:
                    pathto[node]=s
                else:
                    pathto[node]=pathto[parent]+' & ' +s
                
                recurse(tree_.children_left[node], depth + 1, node)
                s="{} > {}".format( name, threshold)
                if node == 0:
                    pathto[node]=s
                else:
                    pathto[node]=pathto[parent]+' & ' +s
                recurse(tree_.children_right[node], depth + 1, node)
            else:
                k=k+1
                print(k,')',pathto[parent], tree_.value[node])
                rule = str(pathto[parent]) + str(tree_.value[node])
                rule_all.append(rule)
        recurse(0, 1, 0)
        return rule_all
if __name__ == '__main__':
    #test1:分层抽样
    z = Sample.group_sample(data, label, frac = 1/3)
        
            