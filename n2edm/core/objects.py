from ..abstract.objects import *
from ..models.models import *
from copy import copy
import random


class Object(IObject):

    model = None
    _set_id = None
    objects = []
    max_pos = 0

    def __init__(self, *args, **kwargs):
        self.name = None
        self.pk = None
        self.state = None
        Object._set_id = kwargs.get("set_id", id(Object))

        if args:
            (self.name) = args
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
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def create(cls, handler, *args, **kwargs):
        obj = cls(*args, **kwargs)
        check = handler(obj)
        if check:
            obj.state = "to_create"
            cls.objects.append(obj)
        cls.max_pos += 1
        return obj if check else None

    @classmethod
    def update(cls, obj, *args, **kwargs):
        for arg, value in kwargs.items():
            if not hasattr(cls, arg):
                raise TypeError(f"'{cls} attribute': '{arg}'' does not exist!")
            setattr(obj, arg, value)
        obj.state = "to_update"
        return obj

    @classmethod
    def delete(cls, obj, mark=False):
        # TODO: Cascade deletion for GroupObject and ActionObject - Juliusz Task
        if obj.state == "to_create":
            return cls.objects.pop(cls.objects.index(obj))
        obj.state = "to_delete"
        if mark:
            return cls.objects.pop(cls.objects.index(obj))

    @classmethod
    def all(cls):
        if cls == Object:
            return cls.objects
        return (obj for obj in cls.objects if type(obj) == cls)

    @classmethod
    def get(cls, *args, **kwargs):
        rv = None
        for obj in cls.all():
            for kwarg, value in kwargs.items():
                key = f"_{kwarg}"
                if key not in vars(obj).keys():
                    raise AttributeError(f"'{cls}' don't have attribute '{key}'!")
                elif value != vars(obj).get(key):
                    break

            rv = obj
        return rv

    @classmethod
    def filter(cls, *args, **kwargs):
        found = True
        for obj in cls.all():
            for kwarg, value in kwargs.items():
                key = f"_{kwarg}"
                if key not in vars(obj).keys():
                    raise AttributeError(f"'{cls}' don't have attribute '{key}'!")
                elif value != vars(obj).get(key):
                    found = False

            if found:
                yield obj

    @classmethod
    def clear(cls, *args, **kwargs):
        for obj in cls.all():
            mark = True if obj.state == None else False
            cls.delete(obj, mark)


class GroupObject(Object, IGroupObject):

    model = Group

    @classmethod
    def create(cls, handler, *args, **kwargs):

        print(handler.max_pos)

        print("dupa")
        super().create(handler, args, kwargs)

    def __init__(self, *args, **kwargs):
        self.position = None
        super().__init__(*args, **kwargs)

    @property
    def children(self):
        return ActionObject.filter(group=self)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @classmethod
    def delete(cls, obj, mark=False):
        for child in reversed(list(obj.children)):
            child.delete(child)
        super().delete(obj, mark)


class ActionObject(GroupObject, IActionObject):

    model = Action

    def __init__(self, *args, **kwargs):
        self.group = None
        self.start_cmd = None
        self.stop_cmd = None
        self.duration = None
        self.color = None
        self.params = None
        self.position = None
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

    model = Actor

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
