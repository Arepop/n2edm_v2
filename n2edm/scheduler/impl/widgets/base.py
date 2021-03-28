from PyQt5 import QtWidgets, QtCore, QtGui

from .sheduler import Scheduler
from .actions import Actions

from ....widgets.views import BaseView

class Base(BaseView):
    def __init__(self):
        super().__init__()
        self.create_view()

    def create_view(self):
        self.actions = Actions(self)
        self.scheduler = Scheduler(self)
        self.split_widget.addWidget(self.scheduler)
        self.split_widget.addWidget(self.actions)
