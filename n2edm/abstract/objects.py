from abc import ABC, abstractmethod, abstractclassmethod

class IObject(ABC):

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("You need to implement 'name' property!")

    @name.setter
    @abstractmethod
    def name(self):
        raise NotImplementedError("You need to implement 'name' property setter!")

    @abstractclassmethod
    def create(cls):
        raise NotImplementedError("You need to implement 'create' method!")        

    @abstractclassmethod
    def get(cls):
        raise NotImplementedError("You need to implement 'get' method!")

    @abstractclassmethod
    def update(cls):
        raise NotImplementedError("You need to implement 'update' method!")

    @abstractclassmethod
    def delete(cls):
        raise NotImplementedError("You need to implement 'remove' method!")

    @abstractclassmethod
    def filter(cls):
        raise NotImplementedError("You need to implement 'filter' method!")


class IGroupObject(IObject):
    
    @property
    @abstractclassmethod
    def children(self):
        raise NotImplementedError("You need to implement 'children' getter method!")

class IActionObject(IObject):

    @property
    @abstractclassmethod
    def children(self):
        raise NotImplementedError("You need to implement 'children' getter method!")

    @property
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'group' getter method!")

    @group.setter
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'setter' getter method!")

class IActorObject(IObject):
    @property
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'group' getter method!")

    @group.setter
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'group' setter method!")

    @property
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' getter method!")

    @action.setter
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' setter method!")

class ITimelineObject(IActorObject):
    @property
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' getter method!")

    @action.setter
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' setter method!")


class IInfinitActorObject(IActorObject):
    @property
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'group' getter method!")

    @group.setter
    @abstractclassmethod
    def group(self):
        raise NotImplementedError("You need to implement 'group' setter method!")

    @property
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' getter method!")

    @action.setter
    @abstractclassmethod
    def action(self):
        raise NotImplementedError("You need to implement 'action' setter method!")