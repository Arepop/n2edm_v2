import sys
import os
import django

def main():
    sys.dont_write_bytecode = True
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "n2edm.settings")
    django.setup()

    from ..core.objects import GroupObject, ActionObject

    group_model_object = GroupObject.model.objects.get(pk=1)
    fields = {field.name: field.value for field in group_model_object._meta.get_fields()}
    print(fields)

if __name__ == "__main__":
    main()
