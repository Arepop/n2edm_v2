from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):
    pass


class GroupHandler(Handler, IGroupHandler):
    def __init__(self):
        self.no_groups = 0

    def check_unique(self, name, set_id):
        names = [group.name for group in GroupObject.filter(set_id=set_id)]
        if name in names:
            raise NameError(
                "GroupObject with that name alredy exist in that set. Choose different name"
            )

    # def set_position(self):
    #     for


class ActionHandler(Handler, IActionHandler):
    pass


class ActorHandler(Handler, IActorHandler):
    pass