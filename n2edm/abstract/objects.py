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
    def delete(cls):
        raise NotImplementedError("You need to implement 'remove' method!")
        
    @abstractclassmethod
    def create(cls):
        raise NotImplementedError("You need to implement 'create' method!")


class IActorObject(IObject):
    pass

class IActionObject(IObject):
    pass

class IGroupObject(IObject):
    pass

class ITimelineObject(IActorObject):
    pass

class IInfinitActorObject(IActorObject):
    pass