import sys
import os
import django

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

from .handlers import *
from .objects import InfinitActorObject


def main():
    print("WOOO2!")
    hand = Handler()
    hand.check_unique(name="12")
    act = ActorHandler()
    infact = InfinitActorHandler()
    # infact.fit_check(act.addd(2.3, 2.4))
    # print(infact.check_infinit(infact))
    actor = InfinitActorObject(name="abc", action="s", group="d")
    infact.check_infinit(actor)
    act.addd(1, 2)
    act.addd(3, 4)
    act.time_check(act.addd(2.3, 2.4))
    act.addd(2.3, 2.4)
    # print(act.check_infinit())


if __name__ == "__main__":
    main()
