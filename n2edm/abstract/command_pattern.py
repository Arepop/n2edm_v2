from abc import ABC, abstractmethod, abstractclassmethod

class ICommand(ABC):
    pass

class IInvoker(ABC):
    pass

class IReciever(ABC):
    pass

class IUndoRedo(ABC):
    pass