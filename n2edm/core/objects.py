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
        obj = Object(name)
        obj._id = id(obj)
        Object.objects.append(obj)

    @classmethod
    def all(cls):
        for obj in Object.objects:
            yield obj


    @classmethod
    def get_id(cls,obj):
        return obj._id

    @classmethod
    def remove(cls):
        Object.objects.pop()

class Group(IGroupObject):
    pass
