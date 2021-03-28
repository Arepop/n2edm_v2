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
    hand = Handler()
    hand.check_unique(name="12")
    act = ActorHandler()
    infact = InfinitActorHandler()
    # infact.fit_check(act.addd(2.3, 2.4))
    # print(infact.check_infinit(infact))
    iactor = InfinitActorObject(name="abc", action="s", group="d", start=1)
    iactor2 = InfinitActorObject(name="abc255", action="s", group="d", start=4)
    iactor3 = InfinitActorObject(name="abc234", action="s", group="d", start=5)

    actor = ActorObject(name="vs", action="asd", group="d", start=1, stop=3)
    infact.object_.objects.append(actor)
    infact.object_.objects.append(iactor)
    # infact.object_.objects.append(iactor2)
    infact.cut_infinit_actor(iactor2)
    infact.object_.objects.append(iactor2)
    infact.check(iactor3)
    infact.cut_infinit_actor(iactor3)

    infact.object_.objects.append(iactor3)

    for a in infact.object_.objects:
        print(a.name)
        print(a.start)
        print(a.stop)

    # print(infact.object_.objects)
    # print(act.object_.objects)
    # print(infact.check_infinit(actor))
    # act.addd(1, 2)infactinfact
    # act.addd(3, 4)
    # act.time_check(act.addd(2.3, 2.4))
    # act.addd(2.3, 2.4)
    # print(act.check_infinit())


if __name__ == "__main__":
    main()
