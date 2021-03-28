from abc import ABC, abstractmethod, abstractclassmethod


class IHandler(ABC):
    pass


class IGroupHandler(IHandler):
    pass


class IActionHandler(IHandler):
    pass


class IActorHandler(IHandler):
    pass


class IInfinitActorHandler(IHandler):
    pass