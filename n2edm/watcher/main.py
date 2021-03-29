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
    obj = ActionObject.create(hand, name="Action", pk=3)
    print(obj.position)
    actor = ActorObject.create(hand, name="vs", action=obj, group="d", start=1, stop=3)
    # obj = ActionObject.create(hand, name="Action", pk=3)

    print(list(Object.filter(group=obj.group, name="Action")))

if __name__ == "__main__":
    main()
