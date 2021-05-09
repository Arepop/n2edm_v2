from PyQt5 import QtWidgets, QtCore, QtGui

from .sheduler import Scheduler
from .actions import Actions

from ....sync_provider.provider import SyncProvider
from ....widgets.views import BaseView
from ....core.handlers import ActionHandler, GroupHandler, ActorHandler, SequenceHandler


class Base(BaseView):
    def __init__(self):
        super().__init__()
        self.sync_provider = SyncProvider()
        self.actor_handler = ActorHandler()
        self.action_handler = ActionHandler()
        self.group_handler = GroupHandler()
        self.sequence_handler = SequenceHandler("sequence")

        self.create_view()
        self.create_menu_bar()
        self.connect_signals_with_slots()

    def create_view(self):
        self.actions = Actions(self)
        self.scheduler = Scheduler(self)
        self.split_widget.addWidget(self.scheduler)
        self.split_widget.addWidget(self.actions)

    def connect_signals_with_slots(self):
        self.create_action.triggered.connect(self.actions.tree.open_action_creation_dialog)
        self.actions.tree.SIG_create_actor.connect(self.scheduler.create_actor)
        self.actions.tree.SIG_create_custom_actor.connect(self.scheduler.create_custom_actor)
        self.pull_action.triggered.connect(self.sync_provider.pull_and_overwrite)
        self.push_action.triggered.connect(self.sync_provider.push)
        self.pull_action.triggered.connect(self.actions.tree.sync_with_db)
        self.create_sequence.triggered.connect(self.sequence_handler.update_sequence)
        self.actions.tree.SIG_object_deleted.connect(self.scheduler.object_deleted)
            
    def create_menu_bar(self) -> None:
        """Initiate menu bar for main window with signals (menu actions) connections to functions in widgets
        """
        main_menu = self.menuBar()
        self.save_actions_as = QtWidgets.QAction("Save actions as...")
        self.load_actions_from = QtWidgets.QAction("Load actions from...")
        self.save_schedule_as = QtWidgets.QAction("Save schedule as...")
        self.load_schedule_from = QtWidgets.QAction("Load schedule from...")

        self.file_menu = main_menu.addMenu("File")
        self.file_menu.addAction(self.save_actions_as)
        self.file_menu.addAction(self.load_actions_from)
        self.file_menu.addAction(self.save_schedule_as)
        self.file_menu.addAction(self.load_schedule_from)

        self.undo_action = QtWidgets.QAction("Undo")
        self.undo_action.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        self.redo_action = QtWidgets.QAction("Redo")
        self.redo_action.setShortcut(QtGui.QKeySequence("Ctrl+Y"))

        self.edit_menu = main_menu.addMenu("Edit")
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)

        self.create_action = QtWidgets.QAction("Add Action")
        self.add_timeline = QtWidgets.QAction("Add Timeline")
        self.pull_action = QtWidgets.QAction("Pull")
        self.push_action = QtWidgets.QAction("Push")

        self.actions_menu = main_menu.addMenu("Actions")
        self.actions_menu.addAction(self.create_action)
        self.actions_menu.addAction(self.add_timeline)
        self.actions_menu.addAction(self.pull_action)
        self.actions_menu.addAction(self.push_action)

        self.create_sequence = QtWidgets.QAction("Create sequence")

        self.sequence_menu = main_menu.addMenu("Sequence")
        self.sequence_menu.addAction(self.create_sequence)

