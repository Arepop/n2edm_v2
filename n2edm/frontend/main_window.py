from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtCore import pyqtSignal as Signal

from .scheduler import ScheduleWindow
from .set_items import SetItemsWindow
from .file_manager import FileManager
from .item_lookup import ItemLookup


def exception_hook(exctype, value, traceback):
    """Error handling cast to Dialog window.

    Args:
        exctype (str): exepion type
        value (str): value of excepiton
        traceback (str): text of exception
    """
    traceback_formated = trs.format_exception(exctype, value, traceback)
    traceback_string = "".join(traceback_formated) + "\n"
    dialog = ErrorDialog(exctype, value, traceback, traceback_string)
    logging.exception(traceback_string)
    dialog.exec()


class MainWindow(QtWidgets.QMainWindow, QtWidgets.QWidget):

    SIG_resized = Signal(object)

    def __init__(self):
        """Initialize all handlers of app"""
        super().__init__()
        self.setWindowTitle("n2EDM Scheduler v. 0.1.0")
        self.create_main_window()
        self.create_view()
        self.create_menu_bar()
        self.make_signals()

    def create_main_window(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        main_layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        self.split_widget = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.set_layout = QtWidgets.QVBoxLayout()
        self.set_widget = QtWidgets.QWidget()
        self.set_widget.setLayout(self.set_layout)
        main_layout.addWidget(self.split_widget)
        self.resize(800, 600)

    def create_view(self):
        """Create main window view"""
        self.set_items = SetItemsWindow(self)
        self.scheduler = ScheduleWindow(self)
        self.file_manager = FileManager(self)
        self.item_lookup = ItemLookup(self)
        self.split_widget.addWidget(self.scheduler)
        self.set_layout.addWidget(self.set_items)
        self.set_layout.addWidget(self.item_lookup)
        self.set_widget.setMaximumWidth(250)
        self.split_widget.addWidget(self.set_widget)

    def create_menu_bar(self) -> None:
        """Initiate menu bar for main window with signals (menu set_items) connections to functions in widgets"""
        main_menu = self.menuBar()
        self.save_set_items_as = QtWidgets.QAction("Save set_items as...")
        self.load_set_items_from = QtWidgets.QAction("Load set_items from...")
        self.save_schedule_as = QtWidgets.QAction("Save schedule as...")
        self.load_schedule_from = QtWidgets.QAction("Load schedule from...")

        self.file_menu = main_menu.addMenu("File")
        self.file_menu.addAction(self.save_set_items_as)
        self.save_set_items_as.triggered.connect(self.file_manager.save_set_items)
        self.file_menu.addAction(self.load_set_items_from)
        self.load_set_items_from.triggered.connect(self.file_manager.load_set_items)
        self.file_menu.addAction(self.save_schedule_as)
        self.save_schedule_as.triggered.connect(self.file_manager.save_schedule)
        self.file_menu.addAction(self.load_schedule_from)
        self.load_schedule_from.triggered.connect(self.file_manager.load_schedule)

        self.undo_action = QtWidgets.QAction("Undo")
        self.undo_action.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        self.redo_action = QtWidgets.QAction("Redo")
        self.redo_action.setShortcut(QtGui.QKeySequence("Ctrl+Y"))

        self.edit_menu = main_menu.addMenu("Edit")
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)

        self.create_action = QtWidgets.QAction("Add Action")
        self.add_timeline = QtWidgets.QAction("Add Timeline")
        self.clear_set_items = QtWidgets.QAction("Clear set_items")
        self.clear_schedule = QtWidgets.QAction("Clear schedule")
        self.pull_action = QtWidgets.QAction("Pull from database")
        self.push_action = QtWidgets.QAction("Push to database")

        self.set_items_menu = main_menu.addMenu("Options")
        self.set_items_menu.addAction(self.create_action)
        self.set_items_menu.addAction(self.add_timeline)
        self.set_items_menu.addAction(self.clear_set_items)
        self.set_items_menu.addAction(self.clear_schedule)

        # self.db_menu = main_menu.addMenu("Database")
        # self.db_menu.addAction(self.pull_action)
        # self.db_menu.addAction(self.push_action)

        self.create_sequence = QtWidgets.QAction("Create sequence")
        self.create_sequence.triggered.connect(self.file_manager.save_sequence)
        self.set_no_cycles = QtWidgets.QAction("Set Number of Cycles")
        self.set_no_cycles.triggered.connect(self.file_manager.set_number_of_cycles)

        self.sequence_menu = main_menu.addMenu("Run")
        self.sequence_menu.addAction(self.create_sequence)
        self.sequence_menu.addAction(self.set_no_cycles)

    def make_signals(self):
        self.set_items.tree.remove_item_event.connect(self.scheduler.remove_items)
        self.set_items.tree.create_schedule_item_event.connect(self.scheduler.add_schedule_item)
        self.set_items.tree.set_items_tree_reloaded_event.connect(self.scheduler.clear)
        self.set_items.tree.set_item_updated_event.connect(self.scheduler.update_items)
        self.file_manager.set_items_loaded_event.connect(self.set_items.tree.bulk_create_items)
        self.file_manager.schedule_loaded_event.connect(self.scheduler.bulk_create_items)

    def resizeEvent(self, event):
        """Resize everything witin app"""
        super().resizeEvent(event)
        self.SIG_resized.emit(event)
