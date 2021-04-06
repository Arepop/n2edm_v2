from PyQt5 import QtWidgets, QtCore, QtGui

from .sheduler import Scheduler
from .actions import Actions

from ....widgets.views import BaseView

class Base(BaseView):
    def __init__(self):
        super().__init__()
        self.create_view()
        self.connect_signals_with_slots()

    def create_view(self):
        self.actions = Actions(self)
        self.scheduler = Scheduler(self)
        self.split_widget.addWidget(self.scheduler)
        self.split_widget.addWidget(self.actions)

    def connect_signals_with_slots(self):
        self.create_action.triggered.connect(self.actions.tree.open_action_creation_dialog)
        self.actions.tree.SIG_create_actor.connect(self.scheduler.create_actor)