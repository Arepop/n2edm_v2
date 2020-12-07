from abc import ABC, abstractmethod, abstractclassmethod


class ICoreDialog(ABC):
    pass

class IGroupDialog(ICoreDialog):
    pass

class IActionDialog(ICoreDialog):
    pass

class ICreateActionDialog(IActionDialog):
    pass

class IUpdateActionDialog(IActionDialog):
    pass

class IDeleteActionDialog(IActionDialog):
    pass

class ITimeDialog(ICoreDialog):
    pass

class ICloseDialog(ICoreDialog):
    pass