from keras.datasets import mnist
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Dense, Activation
import keras
"""
介绍
通过keras 训练mnist
"""

"""
数据加载
"""
(x_train, y_train), (x_test, y_test) = mnist.load_data()

"""
数据探索
"""
x_train.shape #查看shape
x_train.dtype #查看数据类型

"""
数据预处理
"""
#维度变换
x_train = x_train.reshape(60000, 784)
x_train = x_train.astype('float32')
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32')

#y变量one-hot编码,多分类情况
n_classes = 10
y_train = keras.utils.to_categorical(y_train, n_classes)
y_test = keras.utils.to_categorical(y_test, n_classes)

"""
模型训练
"""
#网络参数设置
n_hidden_1 = 256
n_hidden_2 = 256
n_input = 784
training_epochs = 15 #训练次数
batch_size = 100 #每批数据的大小

#建立神经网络
model = Sequential() #顺序模型、多个网络层的线性堆叠
model.add(Dense(n_hidden_1, activation = 'relu', input_dim = 784)) #input_shape = (n, ) 和input_dim = n等价
model.add(Dense(n_hidden_2, activation = 'relu')) #第二层不需要input
model.add(Dense(n_classes, activation = 'softmax')) #最后一层

#编译
model.compile(loss = 'categorical_crossentropy', optimizer = SGD(), metrics = ['accuracy'])

#训练
model.fit(x_train, y_train, epochs = training_epochs, batch_size = batch_size, verbose = 1, validation_data = (x_test, y_test)) #validation_data验证集

