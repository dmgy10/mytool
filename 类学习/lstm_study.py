"""
利用LSTM预测股价
"""


import pandas_datareader
from sklearn.preprocessing import MinMaxScaler
import numpy as np

#数据获取
google = pandas_datareader.get_data_yahoo('GOOGL')

#数据探索
google['Close'].plot(kind = 'line')
google.count()

#划分训练集和测试集
training_set = google.iloc[0:1259 - 200, 4:5].values
test_set = google.iloc[1259 - 200:, 4:5].values

#数据标准化
minmax_scaler = MinMaxScaler(feature_range = (0, 1))

training_set_sca = minmax_scaler.fit_transform(training_set)

#数据预处理、用前60天预测后一天的结果
X_train = []
y_train = []
for i in range(60, len(training_set_sca )):
    X_train.append(training_set_sca[i - 60:i, 0])
    y_train.append(training_set_sca[i, 0])

X_train = np.array(X_train)
y_train = np.array(y_train)



