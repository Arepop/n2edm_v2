import sys
import os
import django


def main():
    sys.dont_write_bytecode = True
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "n2edm.settings")
    django.setup()

    from ..core.objects import GroupObject, ActionObject

    for obj in GroupObject.model.objects.all():
        print(vars(obj))


if __name__ == "__main__":
    main()
