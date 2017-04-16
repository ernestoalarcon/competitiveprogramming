from functools import wraps
from functools import partial
import functools

def logged_call(fun):
    def logged_call_decorator(self, *args, **kwargs):
        print('Before calling {}'.format(fun))
        r = fun(self, *args, **kwargs)
        print('After calling {}'.format(fun))
        return r
    return wraps(fun)(logged_call_decorator)

def my_sum(a, b, c, d):
    return a + b + c + d

sum_5 = partial(my_sum, 5)
print('sum_5(123) yields {}'.format(sum_5(1, 2, 3)))

class CustomError(Exception):
    def __init__(self):
        super().__init__('A custom exception')

class Animal:
    def __init__(self, size, sound):
        self.size = size
        self.sound = sound

    @logged_call
    def do_sound(self):
        print(self.sound)

class Dog(Animal):
    def __init__(self, color):
        super(self.__class__, self).__init__(10, 'Woof, Woof')
        self.color = color

class Cat(Animal):
    def __init__(self, color):
        super(self.__class__, self).__init__(10, 'Meoooouuuu')
        self.color = color

    def play(self, other_animal):
        if isinstance(other_animal, Dog):
            raise CustomError

class Person(object):
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return ' '.join((self.first, self.last))

    @full_name.setter
    def full_name(self, new_full_name):
        self.first, self.last = new_full_name.split(' ')

print(type(functools))

p1 = Person('Ernesto', 'Alarcon')
print('p1.full_name is ', p1.full_name)
p1.full_name = 'Juan Perez'
print('p1.full_name is ', p1.full_name)

a1 = Animal(123, 'my sound')
c1 = Cat('yellow')
d1 = Dog('brown')

a1.do_sound()
c1.do_sound()
d1.do_sound()
c1.play(c1)

# property
# iterator
# custom decorator