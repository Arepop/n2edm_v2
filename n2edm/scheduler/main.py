import sys
import os
import django

def main():
    sys.dont_write_bytecode = True
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "n2edm.settings")
    django.setup()

    from ..core.objects import GroupObject, ActionObject

    group = GroupObject.model.objects.get(pk=1)
    fields = {}
    for field in group._meta.get_fields():
        if field.name == 'action':
            continue
        elif field.name == "id":
            fields['id_'] = field.value_from_object(group)
        else:
            fields[field.name] = field.value_from_object(group)

    GroupObject.create(**fields)
    print(GroupObject.get(id_=1))

if __name__ == "__main__":
    main()
