import lightgbm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
"""
算法介绍：https://www.jianshu.com/p/097ccbec36e4;https://blog.csdn.net/xiaoyi_eric/article/details/80167968
优点1：将连续的特征值离散化成一个个bin，提升了效率，节省了空间
优点2：相较于level-wise，leaf-wise在叶子数量一样时，能降低误差，得到更好地精度，加上限制防止生成深树而在小数据集上造成过拟合
优点3：直接输入类别值，不用one-hot encoding
"""

"""
读入数据
"""
iris = pd.read_excel(r'E:\0_工具\3_数据集\iris.xlsx')

"""
数据预处理
"""
#label映射为数值型0、1、2
label_map = {'setosa':0, 'versicolor':1, 'virginica':2}
iris['Species'] = iris['Species'].map(label_map)

#特征、标签
iris_feature = iris.drop('Species', axis = 1)
iris_label = iris['Species']

#划分训练集
x_train, x_test, y_train, y_test = train_test_split(iris_feature, iris_label, test_size = 0.25)

"""
训练
"""
#模型构建、参数设置
lgb_model = lightgbm.LGBMClassifier()

#模型训练
lgb_model.fit(x_train, y_train)

"""
模型预测
"""
y_pred = lgb_model.predict(x_test)

acc = metrics.accuracy_score(y_test, y_pred) #准确率
confusion_matrix = metrics.confusion_matrix(y_test, y_pred) #混淆矩阵