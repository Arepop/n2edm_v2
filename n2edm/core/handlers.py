from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object

    def __init__(self):
        self.no_object = 0

    @classmethod
    def check_unique(cls, name):

        for obj in cls.object_.all():
            if name == obj.name:
                raise NameError(
                    "Object with that name alredy exist in that set. Choose different name"
                )


class GroupHandler(Handler, IGroupHandler):

    pass


class ActionHandler(Handler, IActionHandler):

    pass


class ActorHandler(Handler, IActorHandler):

    object_ = ActorObject

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
                raise ValueError("zly czas")


class InfinitActorHandler(Handler, IInfinitActorHandler):
    object_ = InfinitActorObject

    def check_infinit(cls, obj):
        for t in cls.object_.filter(group=obj.group):

            if t is type(InfinitActorObject):
                return True
            else:
                return False

    # sprawdza czy aktor którego chce dodać (obj) czy się mieśći
    def fit_check(cls, obj):

        for t in cls.object_.filter(group=obj.group):
            if t.start == obj.start:
                raise ValueError("Cant fit")

        return True

    def cut_infinit_actor(cls, obj):
        pass
