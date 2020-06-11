class MyError(Exception):
    pass

class DBError(Exception):
    pass

raise MyError('this is my error')
raise DBError('this is db error')

from apyori import apriori
data = [['豆奶','莴苣'],
        ['莴苣','尿布','葡萄酒','甜菜'],
        ['豆奶','尿布','葡萄酒','橙汁'],
        ['莴苣','豆奶','尿布','葡萄酒'],
        ['莴苣','豆奶','尿布','橙汁']]
result = list(apriori(transactions=data))


