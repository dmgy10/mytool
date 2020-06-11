from apyori import apriori
import pandas as pd
import re

def comment_preprocessing(data):
    """
    评论预处理:1、去重; 2、去掉标点符号
    :param data: series
    :return:
    """

    # 去重
    comment = data.copy()
    comment_drop_duplicates = comment.drop_duplicates()  # 去重

    # 去掉常见符号
    punc_pattern = ',|\.|\(|\)|\?\!'
    comment_drop_punc = comment_drop_duplicates.map(lambda x: re.sub(punc_pattern, '', x))

    # 去掉多余空格
    comment_drop_whitespace = comment_drop_punc.map(lambda x: re.sub(' +', ' ', x))

    # 去掉前后的空格
    comment_drop_whitespace_beforeafter = comment_drop_whitespace.map(lambda x: x.strip())

    # 全部转换为小写
    comment_to_lower = comment_drop_whitespace_beforeafter.str.lower()

    return comment_to_lower

def split_sentence(data):
    """
    功能：长句分短句
    :param data: series
    :return:
    """

    comment = data.copy()

    # 分句符号
    split_sign_pattern = '\.|,|\?|\!'
    comment_short_sentence = comment.map(lambda x: re.split(split_sign_pattern, str(x))).to_list()

    # 将二维数组转换为一维
    comment_short_sentence_list = [i for j in comment_short_sentence for i in j]

    # 将list输出为series
    return pd.Series(comment_short_sentence_list)

def filter_short_sentence(data):
    """
    功能：过滤掉不是短句的句子
    :param data:
    :return:
    """
    comment = data.copy()
    comment_drop_none = comment[comment != '']

    return comment_drop_none

def data_prepare(data):
    comment = data.copy()
    commment_ = comment.map(lambda x: x.split(' '))

    return  commment_.to_list()


data = pd.read_csv(r'D:\BaiduNetdiskDownload\饮水机.csv')
comment = data.loc[:, '评论']

# 分句
short_sentence = split_sentence(comment)

# 分句过滤
short_sentence_filter = filter_short_sentence(short_sentence)

# 分句预处理
short_sentence_preprocess = comment_preprocessing(short_sentence_filter)

# 数据准备
data_pre = data_prepare(short_sentence_preprocess)

min_supp = 0.2
min_conf = 0.1
min_lift = 1.5
res = apriori(transactions=data_pre[: 100], min_support=min_supp, min_confidence=min_conf, min_lift=min_lift)
res = apriori(transactions=data_pre[: 1000], min_support=0.05)
for i in res:
    print(str(i))
