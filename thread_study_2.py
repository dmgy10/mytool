import time, threading
'''
普通创建方式
'''
def run(n):
    print('task',n)
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=run,args=('t1',))     # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    t2 = threading.Thread(target=run,args=('t2',))
    t1.start()
    t2.start()