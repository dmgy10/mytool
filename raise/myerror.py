class MyError(Exception):
    pass

class DBError(Exception):
    pass


if __name__ == '__mian__':
    raise MyError('this is my error')
    raise DBError('this is db error')



