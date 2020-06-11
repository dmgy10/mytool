def hi(name="yasoob"):
    return "hi " + name

#将函数赋值给变量

hi_2 = hi

#删除原函数
del hi


#在函数中定义函数
def hi(name="yasoob"):
    print("now you are inside the hi() function")

    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    print(greet())
    print(welcome())
    print("now you are back in the hi() function")


hi()

#在函数中返回函数
def hi(name="yasoob"):
    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    if name == "yasoob":
        return greet
    else:
        return welcome


a = hi()
print(a)

#将函数作为一个参数传给另一个函数
def hi():
    return "hi yasoob!"


def doSomethingBeforeHi(func):
    print("I am doing some boring work before executing hi()")
    print(func())

doSomethingBeforeHi(hi)


#第一个装饰器
def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")

a_function_requiring_decoration()
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
a_function_requiring_decoration()


@a_new_decorator
def a_function_requiring_decoration():
    """Hey you! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")


a_function_requiring_decoration()
a_function_requiring_decoration.__name__


#函数参数
def m(*args, **kwargs):
    print(args[0])
    for i, v in kwargs.items():
        print(i, v)


from functools import wraps
def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)

    return with_logging
@logit
def addition_func(x):
    return x + x

result = addition_func(4)


#
from functools import wraps

def first_decorators(func):
    @wraps(func)
    def add_print(*args):
        print('result:')
        return func(*args)
    return add_print

@first_decorators
def add(x, y):
    return x + y

