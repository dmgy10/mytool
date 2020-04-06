"""
super函数学习
"""

class Animal:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def get_study(self):
        print('i can sing')

class People(Animal):
    def __init__(self, legs):
        super().__init__('x', 'y')
        self.legs = legs
    def __test_private(self):
        print('test private method')
class B(Animal):
    def get_ss(self):
        print('xx')

a = People(legs = 2)
b = B()
