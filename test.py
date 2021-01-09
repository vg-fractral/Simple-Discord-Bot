

class Class1:
    def __init__(self, name):
        self.name = name

class Class2():
    def __init__(self, class1):
        self.class1 = class1
    @classmethod
    def maker(cls, name):
        return cls(Class1(name))

object = Class2.maker("John")
print(object.class1.name)