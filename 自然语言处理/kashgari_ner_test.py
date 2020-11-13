# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:51:17 2019

@author: majk1
"""

import pickle,os

with open('words_tag_data.pkl','rb') as ipt:
    title_cut_all = pickle.load(ipt)
    tag_all = pickle.load(ipt)

from sklearn.model_selection import train_test_split
x_train,x_test, y_train, y_test = train_test_split(title_cut_all, tag_all, test_size=0.2, random_state=43)
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train,  test_size=0.2, random_state=43)

import kashgari
from kashgari.embeddings import BERTEmbedding

bert_embed = BERTEmbedding('/root/meicloud/majk1/NLP/BERT/chinese_L-12_H-768_A-12',
                           task=kashgari.LABELING,
                           sequence_length=100)

from kashgari.tasks.labeling import BiLSTM_CRF_Model

model = BiLSTM_CRF_Model(bert_embed)
model.fit(x_train,
          y_train,
          x_validate=x_valid,
          y_validate=y_valid,
          epochs=10,
          batch_size=512)
          
          