from ..abstract.objects import *
from ..models.models import Group, Action

class Object(IObject):

    model = None
    set_id = None
    objects = []

    def __init__(self, *args, **kwargs):
        self.name = None
        self.id_ = None
        Object.set_id = kwargs.get("set_id", id(Object))

        if args:
            self.name, = args
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                setattr(self, arg, value)

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
        obj = cls(*args, **kwargs)
        obj.id_ = kwargs.get("id_", id(obj))
        cls.objects.append(obj)
        return obj

    @classmethod
    def all(cls):
        return (obj for obj in cls.objects if isinstance(obj, cls))

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
            if not hasattr(cls, str(arg)):
                raise TypeError(f"'{cls} attribute': '{arg}'' does not exist!")
            for obj in cls.all():
                prop = getattr(cls, arg)
                if value == prop.fget(obj):
                    yield obj
           
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

    model = Group

    def __init__(self, *args, **kwargs):
        self._check_unique(kwargs.get('name'), kwargs.get('set_id'))
        super().__init__(*args, **kwargs)

    @property
    def children(self):
        return ActionObject.filter(group=self)

    def _check_unique(self, name, set_id):
        names = [(group.name, group.set_id) for group in GroupObject.all()]
        if name in names:
            raise NameError("GroupObject with that name alredy exist in that set. Choose different name")
        
    def save(self):
        db_item = self.model.objects.create(set_id=self.set_id, name=self.name)
        db_item.save()
        self.id_ = db_item.id

class ActionObject(Object, IActionObject):

    model = Action

    def __init__(self, *args, **kwargs):
        self.group = None
        self.set = None
        super().__init__(*args, **kwargs)

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
    def __init__(self,  *args, **kwargs):
        self.group = None
        self.action = None
        super().__init__( *args, **kwargs)

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