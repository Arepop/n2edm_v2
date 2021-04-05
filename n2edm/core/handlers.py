from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object
    max_pos = 0

    def __init__(self):
        self.no_object = 0

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

        super().__init__(*args, **kwargs)

    @classmethod
    def test(cls):
        print("test")
        for i in GroupObject.all():
            print(i.name)
            print(i.position)

    @classmethod
    def swap_position(cls, obj1, obj2):
        temp = obj1.position
        obj1.position = obj2.position
        obj2.postion = temp


class ActionHandler(Handler, IActionHandler):
    object_ = ActionObject


class ActorHandler(Handler, IActorHandler):

    object_ = ActorObject

    @classmethod
    def check(cls, obj):

        # cls.check_unique(obj)
        cls.time_check(obj)

        return True

    def __call__(self, obj):
        return self.check(obj)

    @classmethod
    def time_check(cls, obj):

        for old_obj in cls.object_.filter(group=obj.group):
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