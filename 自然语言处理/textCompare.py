# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 23:34:21 2020

@author: kerui
"""


def levenshtein(str1, str2):
    matrix = [[i + j for j in range(len(str1) + 1)] for i in range(len(str2) + 1)]
    # print(matrix)
    # print("=============")
    for i in range(1, len(str2) + 1):
        for j in range(1, len(str1) + 1):
            if str1[j - 1] == str2[i - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
    # print(matrix)

    
    
    str1mark = ''
    str2mark = ''
    indexI = len(str2)
    indexJ = len(str1)
# 从右下角单元格回溯，若Ai=Bj，则回溯到左上角单元格；
# 若ai≠bj，回溯到左上角、上边、左边中值最小的单元格，
# 若有相同最小值的单元格，优先级按照左上角、上边、左边的顺序。
# 若回溯到左上角单元格，将Ai添加到匹配字串A，将Bj添加到匹配字串B；
# 若回溯到上边单元格，将Bi添加到匹配字串B，将_添加到匹配字串A；
# 若回溯到左边单元格，将_添加到匹配字串B，将Aj添加到匹配字串A；

    if str1[indexJ-1] == str2[indexI-1]:
        str1mark = "\033[0m" +str1[indexJ-1] + str1mark
        str2mark = "\033[0m" +str2[indexI-1] + str2mark
        indexI -= 1
        indexJ -= 1

    for i in range(1, len(str1) + len(str2) + 1):
        print(indexI,indexJ)
        if indexI == 0 and indexJ == 0:
            break
        elif indexI == 0:
            str1mark = '\033[1;31m' + str1[indexJ-1] + str1mark
            str2mark = '\033[1;31m' + '_' + str2mark
            indexJ -= 1
        elif indexJ == 0:
            str1mark = '\033[1;31m' + '_' + str1mark
            str2mark = '\033[1;31m' + str2[indexI-1] + str2mark
            indexI -= 1
        else:
            minnum = min(matrix[indexI - 1][indexJ - 1], matrix[indexI][indexJ - 1], matrix[indexI - 1][indexJ])
            if matrix[indexI - 1][indexJ - 1] == minnum:
                str1mark = str1[indexJ-1] + str1mark
                str2mark = str2[indexI-1] + str2mark
                if str1[indexJ-1] == str2[indexI-1]:
                    str1mark = "\033[0m" + str1mark
                    str2mark = "\033[0m" + str2mark
                else:
                    str1mark = '\033[1;31m' + str1mark
                    str2mark = '\033[1;31m' + str2mark
                indexI -= 1
                indexJ -= 1
            elif matrix[indexI - 1][indexJ] == minnum:
                str1mark = '\033[1;31m'+'_' + str1mark
                str2mark = '\033[1;31m'+str2[indexI-1] + str2mark
                indexI -= 1
            elif matrix[indexI][indexJ - 1] == minnum:
                str1mark = '\033[1;31m'+str1[indexJ-1] + str1mark
                str2mark = '\033[1;31m'+'_' + str2mark
                indexJ -= 1
            
    print(str1mark)
    print(str2mark)
    
       
    return matrix[len(str2)][len(str1)]


if __name__ == '__main':
    a="17.3如发包方有证据认为承包方无法完全履行本合同而承包方无法提供有效的担保时,"
    b="173如发包方有证虽“为采包方无法完全用行木合同而承包方无法提供有效的担保时"


    # test1 两个完全一致
    text1 = '证据认为承包方'
    text2 = '证据认为承包方证据认为承包方证据认为承包方'

    # test2 字符串内容一致、有重复
    text1 = '证据认为承包方'
    text2 = '证据认为承包方证据认为承包方证据认为承包方'

    # test3 字符串内容一致、有重复
    text1 = '承包方证据证据认为承包方承包方证据'
    text2 = '证据认为承包方证据认为承包方证据认为承包方'

    # test4 有差异的字符串
    text1 = '承包方证据证据认为承包方承包方证据'
    text2 = '提供有效的担保时证据认为提供有效的担保时承包方'

    text1 = '承方证据证据认为承包方承包方！证据'
    text2 = '承包方证证据。认为承包方承包方，q证据'
    c = levenshtein(text1, text2)
    print("\033[0m" ,c)
