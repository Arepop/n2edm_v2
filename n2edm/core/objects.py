from ..abstract.objects import *
from ..models.models import *


class Object(IObject):

    model = None
    set_id = None
    objects = []
    deleted_objects = []
    max_pos = 0
    handler = None

    def __init__(self, *args, **kwargs):
        self.name = None
        self.pk = None
        self.state = None
        Object.set_id = kwargs.get("set_id", id(Object))

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
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        check = cls.handler(obj)
        if check:
            obj.state = "to_create"
            cls.objects.append(obj)
        return obj if check else None

    def update(self, *args, **kwargs):
        old_name = self.name
        self.name = kwargs.get("name")
        check = self.handler(self)
        if check:
            for arg, value in kwargs.items():
                if not hasattr(self, arg):
                    raise TypeError(f"'{self} attribute': '{arg}'' does not exist!")
                setattr(self, arg, value)

            self.state = "to_update"
        else:
            self.name = old_name
        return self  # if check else None

    def delete(self):
        self.handler.free_position(self)
        self.objects.pop(self.objects.index(self))
        self.deleted_objects.append(self)

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
                    rv = None
                    break
                else:
                    rv = obj
            if rv:
                break
        return rv

    @classmethod
    def filter(cls, *args, **kwargs):
        for obj in cls.all():
            found = True
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
            obj.delete()


class GroupObject(Object, IGroupObject):

    model = Group

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
        for child in self.children:
            child.position = self.position

    def delete(self):
        for child in reversed(list(self.children)):
            child.delete()
        super().delete()


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
        return self._stop_cmd

    @stop_cmd.setter
    def stop_cmd(self, stop_cmd):
        self._stop_cmd = stop_cmd

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
        self.position = None
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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position


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

