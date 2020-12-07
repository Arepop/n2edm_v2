from abc import ABC, abstractmethod, abstractclassmethod


class IBaseView(ABC):
    pass

class IScheduleView(IBaseView):
    pass

class ITreeView(IBaseView):
    pass

class IWatcherView(IBaseView):
    pass

class ICycleView(IBaseView):
    pass

class IToolbarView(IBaseView):
    pass

class IMenuView(IBaseView):
    pass

class ISearchBarView(IBaseView):
    pass