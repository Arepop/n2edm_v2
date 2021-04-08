from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object
    max_pos = 0

    def __init__(self):
        self.no_object = 0
        Handler.max_pos = 0
        self.object_.handler = self

    def __call__(self, obj):
        return self.check_unique(obj)

    @classmethod
    def check_unique(cls, obj):
        if type(obj) == GroupObject:
            for other_obj in cls.object_.filter(name=obj.name):
                if obj.name == other_obj.name and obj != other_obj:
                    raise NameError(
                        "Object with that name alredy exist in that set. Choose different name"
                    )
        else:
            for other_obj in cls.object_.filter(group=obj.group):
                if obj.name == other_obj.name and obj != other_obj:
                    raise NameError(
                        "Object with that name alredy exist in that set. Choose different name"
                    )

        return True

    def __call__(self, obj):
        return self.check_unique(obj)


class GroupHandler(Handler, IGroupHandler):
    object_ = GroupObject

    def __init__(self, *args, **kwargs):
        Handler.max_pos = 0
        super().__init__(*args, **kwargs)
        self.object_.handler = self

    def set_position(self, obj):
        obj.position = Handler.max_pos
        Handler.max_pos += 1

    def free_position(self, obj):

        for lower in obj.all():

            if lower.position > obj.position and lower.hand == obj.hand:
                lower.position -= 1
        Handler.max_pos -= 1

    @classmethod
    def swap_position(cls, obj1, obj2):
        temp = obj1.position
        obj1.position = obj2.position
        obj2.postion = temp


class ActionHandler(Handler, IActionHandler):
    object_ = ActionObject

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_.handler = self

    def set_position(self, obj):
        obj.position = Handler.max_pos
        Handler.max_pos += 1

    def free_position(self, obj):

        for lower in obj.all():

            if lower.position > obj.position and lower.hand == obj.hand:
                lower.position -= 1
        Handler.max_pos -= 1

    @classmethod
    def swap_position(cls, obj1, obj2):
        temp = obj1.position
        obj1.position = obj2.position
        obj2.postion = temp


class ActorHandler(Handler, IActorHandler):

    object_ = ActorObject

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_.handler = self

    @classmethod
    def check(cls, obj):

        return True

    def __call__(self, obj):
        return self.check(obj)

    def set_position(self, obj):
        obj.position = Handler.max_pos
        Handler.max_pos += 1

    def free_position(self, obj):

        for lower in obj.all():

            if lower.position > obj.position and lower.hand == obj.hand:
                lower.position -= 1
        Handler.max_pos -= 1

    def __init__(self, *args, **kwargs):
        Handler.max_pos = 0
        super().__init__(*args, **kwargs)

    @classmethod
    def swap_position(cls, obj1, obj2):
        temp = obj1.position
        obj1.position = obj2.position
        obj2.postion = temp

    @classmethod
    def time_check(cls, obj):

        for old_obj in obj.filter(group=obj.group):
            if old_obj == obj:
                continue

            elif (
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
                raise ValueError("You can't create infinity actor with this start")

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