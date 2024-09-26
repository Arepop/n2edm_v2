from abc import ABC, abstractmethod, abstractclassmethod


class IBaseItem(ABC):
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


class IGroupItem(IBaseItem):
    def children(self):
        raise NotImplementedError("You need to implement 'children' getter method!")


class ISetItem(IBaseItem):
    @abstractclassmethod
    def children(self):
        raise NotImplementedError("You need to implement 'children' getter method!")


class IScheduleItem(IBaseItem):
    pass

class ITimelineItem(IScheduleItem):
    pass


class IContinousScheduleItem(IScheduleItem):
    pass