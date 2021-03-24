from ..core.objects import *

class SyncProvider:
    def __init__(self):
        self.auth = True
        self.login = None
        self.passwd = None
        self.adress = None
        self.synced = False
        self.sync_time = "now"

    def connect(self, adress):
        self.adress = adress
        #TODO connection to database/server

    def sync(self):
        if not self.auth:
            raise ConnectionError("Could not connect to server")

        for obj in Object.filter(state="to_create"):
            input_kwargs = self.create_input_dict(obj)
            db_obj = obj.model.objects.create(**input_kwargs)
            obj.state = None
            obj.pk = db_obj.id
        
        for obj in Object.filter(state="to_update"):
            input_kwargs = self.create_input_dict(obj)
            db_obj = obj.model.objects.update(**input_kwargs)
            obj.state = None
            obj.pk = db_obj.id

        for obj in Object.filter(state="to_delete"):
            obj.delete(id=obj.pk, mark=True)
            if obj.pk != None:
                obj.model.objects.all().delete()

    def create_input_dict(self, obj):
        prop_dict = {'set_id': obj.set_id}
        for key, value in vars(obj).items():
            if key[0] == "_":
                prop_dict[key[1:]] = value
            else:
                prop_dict[key] = value

        del prop_dict['pk']
        del prop_dict['state']
        return prop_dict
