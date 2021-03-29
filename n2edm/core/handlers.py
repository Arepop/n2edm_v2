from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object

    def __init__(self):
        self.no_object = 0

    @classmethod
    def check_unique(cls, obj):
        for other_obj in cls.object_.all():
            if obj.name == other_obj.name and obj != other_obj:
                raise NameError(
                    "Object with that name alredy exist in that set. Choose different name"
                )

        return True

    @classmethod
    def __call__(cls, obj):
        check_unique(obj)


class GroupHandler(Handler, IGroupHandler):
    pass


class ActionHandler(Handler, IActionHandler):
    object_ = ActionObject


class ActorHandler(Handler, IActorHandler):

    object_ = ActorObject

    @classmethod
    def check(cls, obj):

        cls.check_unique(obj.name)
        cls.time_check(obj)

    @classmethod
    def __call__(cls, obj):
        check(obj)
        print("check!")

    @classmethod
    def check_unique(cls, name):

        for obj in cls.object_.filter(group=obj.group):
            if name == obj.name:
                raise NameError(
                    "Object with that name alredy exist in that set. Choose different name"
                )

    @classmethod
    def time_check(cls, obj):

        for t in cls.object_.filter(group=obj.group):
            if t == obj:
                continue

            if (
                (obj.start >= t.start and obj.start <= t.stop)
                or (obj.stop >= t.start and obj.stop <= t.stop)
                or (t.start >= obj.start and t.start <= obj.stop)
                or (t.stop >= obj.stop and t.stop <= obj.stop)
            ):
                raise ValueError("Time already in use!")


class InfinitActorHandler(Handler, IInfinitActorHandler):
    object_ = InfinitActorObject

    def __init__(self, *args, **kwargs):
        print("init")

    def __call__(self, obj):
        self.check(obj)
        print("check")

    def check_infinit(cls, obj):
        for t in cls.object_.filter(group=obj.group):

            if t is type(InfinitActorObject):
                return True
            else:
                return False

    @classmethod
    def fit_check(cls, obj):

        for t in cls.object_.filter(group=obj.group):
            if t.start == obj.start:
                raise ValueError("Cant fit")

        return True

    @classmethod
    def cut_infinit_actor(cls, obj):
        cls.check(obj)
        for t in cls.object_.filter(group=obj.group):
            print(t)
            if t.start <= obj.start:
                t.stop = obj.start

    @classmethod
    def check(cls, obj):
        cls.check_unique(obj)
        cls.fit_check(obj)