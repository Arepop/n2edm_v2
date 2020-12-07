from ..abstract.objects import *


class Object(IObject):

    objects = []

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def create(cls, name):
        object = Object(name)
        object._id = 
        Object.objects.append(object)

    @classmethod
    def remove(cls):
        Object.objects.pop()

class Group(IGroupObject):
    pass
