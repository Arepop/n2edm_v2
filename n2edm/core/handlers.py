from ..abstract.handlers import *
from .objects import *


class Handler(IHandler):

    object_ = Object
    current_position = 0

    def __init__(self):
        self.no_object = 0
        Handler.current_position = 0
        self.object_.handler = self

    def __call__(self, obj):
        return self.check(obj)

    @classmethod
    def check(cls, obj):
        cls.check_unique(obj)
        return True

    @classmethod
    def check_unique(cls, obj):
        if type(obj) == GroupObject:
            for other_obj in cls.object_.filter(name=obj.name):
                if obj.name == other_obj.name and obj != other_obj:
                    raise NameError(
                        "Group with that name alredy exist in that set. Choose different name"
                    )
        else:
            for other_obj in cls.object_.filter(group=obj.group):
                if obj.name == other_obj.name and obj != other_obj:
                    raise NameError(
                        f"{cls} with that name alredy exist in that set. Choose different name"
                    )

        return True


class GroupHandler(Handler, IGroupHandler):
    object_ = GroupObject

    def __init__(self, *args, **kwargs):
        Handler.max_pos = 0
        super().__init__(*args, **kwargs)
        self.object_.handler = self

    @classmethod
    def check(cls, obj):
        return True
    
    @classmethod
    def set_position(cls, obj):
        obj.group.position = Handler.current_position
        Handler.current_position += 1
        for child in obj.group.children:
            child.position = obj.group.position

    def free_position(self, obj):

        for lower in obj.all():

            if lower.position < obj.position and lower.handler == obj.handler:
                lower.position -= 1
        Handler.current_position -= 1

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

    @classmethod
    def check(cls, obj):
        return True

    @classmethod
    def set_position(cls, obj):
        if obj.group == None:
            obj.action.position = Handler.current_position
            Handler.current_position += 1          
        else:
            GroupHandler.set_position(obj)

    def free_position(self, obj):
        for lower in obj.all():

            if lower.position < obj.position and lower.handler == obj.handler:
                lower.position -= 1
        Handler.current_position -= 1

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
        cls.calculate_horizontal_position(obj)
        cls.time_check(obj)
        cls.set_position(obj)
        return True

    def __call__(self, obj):
        return self.check(obj)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def swap_position(cls, obj1, obj2):
        temp = obj1.position
        obj1.position = obj2.position
        obj2.postion = temp

    @classmethod
    def time_check(cls, obj):
        if obj.stop == 0 and obj.stop == 0:
            return

        important_objects = obj.filter(group=obj.group) if obj.group else obj.filter(action=obj.action)

        for old_obj in important_objects:
            if old_obj == obj:
                continue

            elif (
                (obj.start >= old_obj.start and obj.start < old_obj.stop)
                or (obj.stop >= old_obj.start and obj.stop <= old_obj.stop)
                or (old_obj.start >= obj.start and old_obj.start < obj.stop)
                or (old_obj.stop >= obj.stop and old_obj.stop <= obj.stop)
            ):
                raise ValueError("Time already in use!")

    @classmethod
    def calculate_horizontal_position(cls, obj):
        maximum_position = 0
        if obj.stop != 0:
            return maximum_position
        if obj.action.group == None:
            maximum_position = max(list(actor.stop for actor in obj.action.children), default=0)
        elif len(list(ActorObject.filter(group=obj.group))):
            maximum_position = max(list(actor.stop for actor in ActorObject.filter(group=obj.group)), default=0)

        obj.start = maximum_position
        obj.stop = maximum_position + obj.action.duration
        return maximum_position


    @classmethod
    def set_position(cls, obj):
        if obj.action.position == None:
            ActionHandler.set_position(obj)
            obj.position = obj.action.position
        else:
            obj.position = obj.action.position

    def free_position(self, obj):
        for lower in obj.all():

            if lower.position < obj.position and lower.handler == obj.handler:
                lower.position -= 1
        Handler.current_position -= 1

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


class SequenceHandler:
    def __init__(self, name):
        self.name = name
        with open(name, "w") as file:
            pass

    def decode(self):
        commands_list = []
        llist = []
        for actor in ActorObject.all():
            commands_list.append((actor.start, actor.action.start_cmd))
            commands_list.append((actor.stop, actor.action.stop_cmd))

        commands_list.sort(key=self.sort_criteria)
        h = commands_list[0][0]
        llist.append("SELLP:" + str(h) + "\n")
        for line in commands_list:
            if line[0] != h:
                llist.append("SELLP" + str(line[0] - int(h)) + "\n")
                h = line[0]
            llist.append(str(line[1]) + "\n")
        print(llist)
        rv_list = [str(_[1]) + "\n" for _ in commands_list]
        return llist

    def sort_criteria(self, command):
        return command[0]

    def update_sequence(self):
        with open(self.name, "w") as file:
            file.writelines(self.decode())
