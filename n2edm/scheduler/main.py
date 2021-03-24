import sys
import os
import django


sys.dont_write_bytecode = True
os.environ['DJANGO_SETTINGS_MODULE'] = 'n2edm.settings'
django.setup()

from ..core.objects import *

def main():

    from ..sync_provider.provider import SyncProvider 

    sync_provider = SyncProvider()

    obj = GroupObject.create(name="dupe", position=1)
    x = GroupObject.filter(set_id=GroupObject.set_id)
    sync_provider.sync()
    qs = GroupObject.model.objects.all()
    print(obj.pk)
    print(list(Object.filter(pk=obj.pk)))
    obj.delete(id=obj.pk)
    sync_provider.sync()
    qs = GroupObject.model.objects.all()
    print(list(qs))

if __name__ == "__main__":
    main()
