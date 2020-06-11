class animal:
    def __init__(self, name):
        self.name = name
    def walk(self):
        return 'walk'

class people(animal):
    def __init__(self, voice):
        super().__init__(name = 'duck')
        self.voice = voice
    def walk(self):
        return 'people'



p = people(voice = 'nice')
p.name



class Test:
    def __init__(self):
       self.foo = 11
       self._bar = 23
       self.__baz = 23

    def _test(self):
        print('this is method')

t =

class ExtendedTest(Test):

   def __init__(self):

       super().__init__()

       self.foo = 'overridden'

       self._bar = 'overridden'

       self.__baz = 'overridden'

t2 = ExtendedTest()