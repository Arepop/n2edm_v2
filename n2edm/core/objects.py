from ..abstract.objects import *
from ..models.models import Group, Action


class Object(IObject):

    model = None
    set_id = None
    objects = []

    def __init__(self, *args, **kwargs):
        self.name = None
        self.pk = None
        Object.set_id = kwargs.get("set_id", id(Object))

        if args:
            (self.name,) = args
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                setattr(self, arg, value)

    @property
    def item(self):
        if self.pk:
            return self.model.objects.get(pk=self.pk)
        return None

    @property
    def pk(self):
        return self._pk

    @pk.setter
    def pk(self, new_id):
        self._pk = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
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
        obj = cls.get(pk=id)
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
        self.position = None
        super().__init__(*args, **kwargs)

    @property
    def children(self):
        return ActionObject.filter(group=self)

    # def save(self):
    #     db_item = self.model.objects.create(set_id=self.set_id, name=self.name)
    #     db_item.save()
    #     self.pk = db_item.id


class ActionObject(Object, IActionObject):

    model = Action

    def __init__(self, *args, **kwargs):
        self.group = None
        self.set = None
        self.start_cmd = None
        self.stop_cmd = None
        self.duration = None
        self.color = None
        self.params = None
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

    @property
    def start_cmd(self):
        return self._start_cmd

    @start_cmd.setter
    def start_cmd(self, start_cmd):
        self._start_cmd = start_cmd

    @property
    def stop_cmd(self):
        return self._start_cmd

    @start_cmd.setter
    def stop_cmd(self, start_cmd):
        self._start_cmd = start_cmd

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params


class ActorObject(Object, IActorObject):
    def __init__(self, *args, **kwargs):
        self.group = None
        self.action = None
        self.color = None
        self.params = None
        self.start = None
        self.stop = None
        self.annotate = None
        self.text = None
        super().__init__(*args, **kwargs)

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

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = stop

    @property
    def annotate(self):
        return self._annotate

    @annotate.setter
    def annotate(self, annotate):
        self._annotate = annotate

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text


class TimelineObject(Object, ITimelineObject):
    def __init__(self, name):
        super().__init__(name)


class InfinitActorObject(Object, IInfinitActorObject):
    def __init__(self, *args, **kwargs):
        self.group = None
        self.action = None
        self.color = None
        self.params = None
        self.start = None
        self.stop = None
        self.annotate = None
        self.text = None
        super().__init__(*args, **kwargs)


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

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = stop

    @property
    def annotate(self):
        return self._annotate

    @annotate.setter
    def annotate(self, annotate):
        self._annotate = annotate

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
