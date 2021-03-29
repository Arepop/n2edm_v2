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
    obj = ActionObject.create(check, name="Action", pk=3)
    actor = ActorObject.create(check, name="vs", action=obj, group="d", start=1, stop=3)

    print(ActionObject.get(group=obj.group, name="Action"))

if __name__ == "__main__":
    main()
