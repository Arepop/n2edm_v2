import sys
import os
import django

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from ..core.handlers import *
from ..core.objects import *


def check(obj):
    return True


def main():
    print("WOOO2!")
    hand = Handler()
    # hand.check_unique(name="12")
    # act = ActorHandler()
    action = ActionObject.create(hand, name="24234", pk=23, group="abv")

    print(list(action.filter(group=action.group)))

    infact = InfinitActorHandler()
    infact(action)

    iactor = InfinitActorObject(name="abc", action="s", group="d", start=1)
    iactor2 = InfinitActorObject(name="abc255", action="s", group="d", start=4)
    iactor3 = InfinitActorObject(name="abc234", action="s", group="d", start=5)
    actor = ActorObject(name="vs", action=action, group="d", start=1, stop=3)


    infact.object_.objects.append(actor)
    infact.object_.objects.append(iactor)
    
    infact.cut_infinit_actor(iactor2)
    infact.object_.objects.append(iactor2)
    infact.check(iactor3)
    infact.cut_infinit_actor(iactor3)

    infact.object_.objects.append(iactor3)



if __name__ == "__main__":
    main()
