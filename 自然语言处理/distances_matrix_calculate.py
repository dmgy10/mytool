# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:24:18 2019

@author: majk1
"""

import numpy as np

def compute_distances_no_loops(X,Y):
    """
    Compute the distance between each test point in X and each training point
    in Y using no explicit loops.

    Input / Output: Same as compute_distances_two_loops
    版权声明：本文为CSDN博主「枯萎的海风」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/zhyh1435589631/article/details/54236643
    """
    num_test = X.shape[0]
    num_train = Y.shape[0]
    dists = np.zeros((num_test, num_train)) 
    dists = np.sqrt(getNormMatrix(X, num_train).T + getNormMatrix(Y, num_test) - 2 * np.dot(X, Y.T))
    return dists

def getNormMatrix(x, lines_num):
    return np.ones((lines_num, 1)) * np.sum(np.square(x), axis = 1) 
