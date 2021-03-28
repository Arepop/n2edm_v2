from abc import ABC, abstractmethod, abstractclassmethod


class IBaseView(ABC):
    pass

class ISchedulerView(IBaseView):
    pass

class IActionsView(IBaseView):
    pass

class IWatcherView(IBaseView):
    pass

class ICycleView(IBaseView):
    pass

class IToolbarView(IBaseView):
    pass

class ISearchBarView(IBaseView):
    pass

class ITreeView(IBaseView):
    pass