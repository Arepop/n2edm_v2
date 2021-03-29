from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object

    def __init__(self):
        self.no_object = 0

    @classmethod
    def check_unique(cls, obj):
        for other_obj in cls.object_.filter(group=obj.group):
            if obj.name == other_obj.name and obj != other_obj:
                raise NameError(
                    "Object with that name alredy exist in that set. Choose different name"
                )

        return True

    def __call__(self, obj):
        return self.check_unique(obj)


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

    def __call__(self, obj):
        return self.check(obj)

    @classmethod
    def check_unique(cls, name):

        for obj in cls.object_.filter(group=obj.group):
            if name == obj.name:
                raise NameError(
                    "Object with that name alredy exist in that set. Choose different name"
                )

    @classmethod
    def time_check(cls, obj):

        for old_obj in cls.object_.filter(group=obj.group):
            if old_obj == obj:
                continue

            if (
                (obj.start >= old_obj.start and obj.start <= old_obj.stop)
                or (obj.stop >= old_obj.start and obj.stop <= old_obj.stop)
                or (old_obj.start >= obj.start and old_obj.start <= obj.stop)
                or (old_obj.stop >= obj.stop and old_obj.stop <= obj.stop)
            ):
                raise ValueError("Time already in use!")


class InfinitActorHandler(Handler, IInfinitActorHandler):
    object_ = InfinitActorObject

    def __call__(self, obj):
        return self.check(obj)

    def check_infinit(cls, obj):
        for old_obj in cls.object_.filter(group=obj.group):

            if old_obj is type(InfinitActorObject):
                return True
            else:
                return False

    @classmethod
    def fit_check(cls, obj):

        for old_obj in cls.object_.filter(group=obj.group):
            if old_obj.start == obj.start:
                raise ValueError("Cant fit")

        return True

    @classmethod
    def cut_infinit_actor(cls, obj):
        cls.check(obj)
        for old_obj in cls.object_.filter(group=obj.group):
            if old_obj.start <= obj.start:
                old_obj.stop = obj.start

    @classmethod
    def check(cls, obj):
        cls.check_unique(obj)
        cls.fit_check(obj)