import sys
import os
import django

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from ..core.handlers import *
from ..core.objects import *


def main():
    print("WOOO2!")
    hand = ActionHandler()
    gh = GroupHandler()
    gh2 = GroupHandler()

    a = GroupObject.create(gh, name="f")
    gh.set_position(a)
    a2 = GroupObject.create(gh, name="f2")
    gh.set_position(a2)

    a3 = GroupObject.create(gh, name="f3")
    gh.set_position(a3)

    a4 = GroupObject.create(gh, name="f4")
    gh.set_position(a4)

    b1 = GroupObject.create(gh2, name="g")

    gh2.set_position(b1)
    b2 = GroupObject.create(gh2, name="g2")
    gh2.set_position(b2)

    b3 = GroupObject.create(gh2, name="g3")
    gh2.set_position(b3)

    # a2.delete(a2)
    a5 = GroupObject.create(gh, name="f5")
    gh.set_position(a5)
    gh.free_position(a5)
    a5.delete(a5)
    # GroupObject.delete(a4)
    a6 = GroupObject.create(gh, name="f6")
    gh.set_position(a6)

    # gh.swap_position(a5, a6)

    # b = Group()
    obj = ActionObject.create(hand, name="Action", pk=3, group=a)
    obj2 = ActionObject.create(hand, name="Action2", pk=33, group=a)
    obj21 = ActionObject.create(hand, name="Action21", pk=33, group=a2)
    # print(obj.name)

    # obj3 = ActionObject.create(hand, name="Action3", pk=333, group=a)
    # obj31 = ActionObject.create(hand, name="Action31", pk=3331, group=a)

    # actor = ActorObject.create(hand, name="vs", action=obj, group="d", start=1, stop=3)

    # gh.test()
    gh2.test()

    # a.test()
    # obj = ActionObject.create(hand, name="Action", pk=3)

    # print(1list(Object.filter(group=obj.group, name="Action")))


if __name__ == "__main__":
    main()
