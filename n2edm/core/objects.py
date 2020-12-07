from ..abstract.objects import *


class Object(IObject):

    objects = []

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def create(cls, name):
        obj = cls(name)
        obj._id = id(obj)
        cls.objects.append(obj)

    @classmethod
    def all(cls):
        for obj in cls.objects:
            yield obj

    @classmethod
    def get_id(cls, obj):
        return obj._id

    @classmethod
    def get(cls, name):
        gen = cls.all()
        for g in gen:
            if g.name == name:
                return g

    @classmethod
    def filter(cls, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                return TypeError(f"'{cls} attribute': '{arg}'' does not exist!")
            for obj in cls.all():
                prop = getattr(cls, arg)
                if value == prop.fget(obj):
                    yield obj

    @classmethod
    def remove(cls):
        cls.objects.pop()


class Group(Object, IGroupObject):
    pass