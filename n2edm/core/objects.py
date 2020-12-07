from ..abstract.objects import *


class Object(IObject):

    objects = []

    def __init__(self, *args, **kwargs):
        self.name = None
        self.id_ = None

        for arg, value in kwargs.items():
            pass

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
    def create(cls, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                raise AttributeError(f"'{cls} attribute': '{arg}' does not exist!")
        obj = cls(args, kwargs)
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
                raise AttributeError(f"'{cls} attribute': '{arg}' does not exist!")
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

    @classmethod
    def update(cls, obj, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                raise TypeError(f"'{cls} attribute': '{arg}'' does not exist!")
            setattr(obj, arg, value)
        return obj


class GroupObject(Object, IGroupObject):
    def __init__(self, name):
        super().__init__(name)

    @property
    def children(self):
        return ActionObject.filter(group=self)


class ActionObject(Object, IActionObject):
    def __init__(self, name, group):
        self.group = None
        super().__init__(name)

    @property
    def children(self):
        return ActorObject.filter(action=self)

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group


class ActorObject(Object, IActorObject):
    def __init__(self, name):
        # group
        self.group = None
        self.action = None
        super().__init__(name)

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action


class TimelineObject(Object, ITimelineObject):
    def __init__(self, name):
        super().__init__(name)


class InfinitActorObject(Object, IInfinitActorObject):
    def __init__(self, name):
        super().__init__(name)