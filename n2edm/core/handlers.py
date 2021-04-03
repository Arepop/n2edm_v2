from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object

    def __init__(self):
        self.no_object = 0

    def __call__(self, obj):
        return self.check_unique(obj)

    @classmethod
    def check_unique(cls, obj):
        if type(obj) == GroupObject:
            for other_obj in cls.object_.filter(name=obj.name):
                if obj.name == other_obj.name:
                    raise NameError(
                        "Object with that name alredy exist in that set. Choose different name"
                    )
        else:
            for other_obj in cls.object_.filter(group=obj.group):
                if obj.name == other_obj.name:
                    raise NameError(
                        "Object with that name alredy exist in that set. Choose different name"
                    )

        return True

    def __call__(self, obj):
        return self.check_unique(obj)


class GroupHandler(Handler, IGroupHandler):
    object_ = GroupObject

    max_pos = len(list(GroupObject.all()))

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    @classmethod
    def test(cls):
        print("elo")
        for i in cls.object_.all():
            print(i.name)

    @classmethod
    def length(cls, obj):
        a = cls.all()
        group_list = []
        for item in a:
            if item.group not in group_list:
                group_list.append(item.group)

        print(group_list)
        return len(group_list)

    @classmethod
    def group_list(cls):
        a = cls.all()
        group_listt = []
        for item in a:
            if item.group not in group_listt:
                group_listt.append(item.group)
        return group_listt

    @classmethod
    def positions(cls):
        ii = 0
        for i in cls.group_list():
            s = cls.filter(group=i)
            for ss in s:
                print(ss.name)
                print(ss.group)
                print(ss.position)

    @classmethod
    def set_positions(cls):
        ii = -1
        for i in cls.group_list():
            print("i")
            print(i)
            print(cls.filter(group=i))

            for ss in cls.filter(group=i):
                ss.position = ii
                print(ss.name)
                print(ss.group)
                print(ss.position)
            ii += 1
            print("stop")

    @classmethod
    def setit(cls):
        print("her")
        for i in AcionObject.all():
            print(i)
        # cls.all().group
        # print(cls.poss[4].name)


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