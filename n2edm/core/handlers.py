from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object

    def __init__(self):
        self.no_object = 0

    @classmethod
    def check_unique(cls, name, set_id):
        names = [cls.object_.name for obj in cls.object_.filter(set_id=set_id)]
        if name in names:
            raise NameError(
                "Object with that name alredy exist in that set. Choose different name"
            )


class GroupHandler(Handler, IGroupHandler):

    pass


class ActionHandler(Handler, IActionHandler):

    pass


class ActorHandler(Handler, IActorHandler):

    pass