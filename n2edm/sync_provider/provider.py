from ..core.objects import *
from ..core.handlers import *

class SyncProvider:
    def __init__(self):
        self.auth = True
        self.login = None
        self.passwd = None
        self.adress = None
        self.synced = False
        self.pull = None
        self.sync_time = "now"        

    def connect(self, adress):
        self.adress = adress
        #TODO connection to database/server

    def sync(self):
        if not self.auth:
            raise ConnectionError("Could not connect to server")
        self.pull = self.pull_and_compare()
        self.push()

    def pull_and_compare(self):
        objects_classes = [GroupObject, ActionObject, ActorObject] #TODO: When InfinityActor and TimelineActor are ready update this
        for elem in objects_classes:
            for obj in elem.model.objects.all():
                attributes = vars(obj)
                self.to_n2edm_objects(attributes)
                yield self.compare(elem, attributes)

    def compare(self, elem, attributes):
        """
        To be implemented in v 2.1.0
        """
        pass 

    def pull_and_overwrite(self):
        objects_classes = [GroupObject, ActionObject, ActorObject] #TODO: When InfinityActor and TimelineActor are ready update this
        for elem in objects_classes:
            for obj in elem.model.objects.all():
                attributes = vars(obj)
                self.to_n2edm_objects(attributes)
                self.overwrite(elem, attributes)

    def overwrite(self, elem, attributes):
        obj = elem.get(pk=attributes["pk"])
        if obj == None:
            obj = elem.create(**attributes)
            obj.state = None
    
        else:
            obj.update(**attributes)

    def push(self):
        for obj in Object.filter(state="to_create"):
            attributes = self.get_attributes(obj)
            db_obj = obj.model.objects.create(**attributes)
            obj.state = None
            obj.pk = db_obj.id

        for obj in Object.filter(state="to_update"):
            attributes = self.get_attributes(obj)
            db_obj = obj.model.objects.filter(id=obj.pk).update(**attributes)
            obj.state = None


        for obj in Object.deleted_objects:
            if obj.pk != None:
                obj.model.objects.get(pk=obj.pk).delete()

    def get_n2edm_model(self, obj):
        return obj.model.objects.get(pk=obj.pk)

    def to_n2edm_models(self, attributes):
        if attributes.get("group"):
            attributes["group"] = self.get_n2edm_model(attributes["group"])
        if attributes.get("action"):
            attributes["action"] = self.get_n2edm_model(attributes["action"])

    def to_n2edm_objects(self, attributes):
        if "group_id" in attributes.keys():
            attributes['group'] = GroupObject.get(pk=attributes.get("group_id"))
            del attributes["group_id"]

        if "action_id" in attributes.keys():
            attributes['action'] = ActionObject.get(pk=attributes.get("action_id"))
            del attributes["action_id"]

        attributes["pk"] = attributes.pop("id")
        del attributes["_state"]

    def get_attributes(self, obj):
        attributes = {}
        for key, value in vars(obj).items():
            attributes[key.strip("_")] = value

        attributes["set_id"] = obj.set_id

        del attributes["pk"]
        del attributes["state"]

        self.to_n2edm_models(attributes)
        return attributes

