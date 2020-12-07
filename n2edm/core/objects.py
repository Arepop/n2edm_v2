from ..abstract.objects import *

class Object(IObject):

    objects = []

    def __init__(self, name):
        self.name = name
        self.id_ = None

    @property
    def id_(self):
        return self._id_

    @id_.setter
    def id_(self, new_id):
        self._id_ = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def create(cls, name):
        obj = cls(name)
        obj.id_ = id(obj)
        cls.objects.append(obj)
        return obj

    @classmethod
    def all(cls):
        if not cls.objects:
            raise IndexError(f"Empty list! First you need to create any object!")
        for obj in cls.objects:
            if isinstance(obj, cls):
                yield obj

    @classmethod
    def get(cls, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                return AttributeError(f"'{cls} attribute': '{arg}' does not exist!")
            for obj in cls.all():
                prop = getattr(cls, arg)
                if value == prop.fget(obj):
                    return obj
        raise IndexError(f"Object of class '{cls}' not found")

    @classmethod
    def filter(cls, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                raise TypeError(f"'{cls} attribute': '{arg}'' does not exist!")
            for obj in cls.all():
                prop = getattr(cls, arg)
                if value == prop.fget(obj):
                    yield obj
        
        raise IndexError(f"Object of class '{cls}' not found")

    
    @classmethod
    def delete(cls, id):
        obj = cls.get(id_=id)
        return cls.objects.pop(cls.objects.index(obj))


class GroupObject(Object, IGroupObject):
    
    def __init__(self, name):
        super().__init__(name)

class ActionObject(Object, IActionObject):
    
    def __init__(self, name):
        super().__init__(name)

class ActorObject(Object, IActorObject):
    
    def __init__(self, name):
        super().__init__(name)

class TimelineObject(Object, ITimelineObject):
    
    def __init__(self, name):
        super().__init__(name)

class InfinitActorObject(Object, IInfinitActorObject):
    
    def __init__(self, name):
        super().__init__(name)