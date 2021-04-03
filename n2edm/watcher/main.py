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

    a = GroupObject.create(gh, name="f")
    a2 = GroupObject.create(gh, name="f2")

    # b = Group()
    obj = ActionObject.create(hand, "Action", pk=3, group=a)
    obj2 = ActionObject.create(hand, name="Action2", pk=33, group=a)
    obj21 = ActionObject.create(hand, name="Action21", pk=33, group=a2)
    print(obj.name)

    # obj3 = ActionObject.create(hand, name="Action3", pk=333, group=a)
    # obj31 = ActionObject.create(hand, name="Action31", pk=3331, group=a)

    # actor = ActorObject.create(hand, name="vs", action=obj, group="d", start=1, stop=3)

    gh.test()
    # a.test()
    # obj = ActionObject.create(hand, name="Action", pk=3)

    # print(1list(Object.filter(group=obj.group, name="Action")))


if __name__ == "__main__":
    main()
