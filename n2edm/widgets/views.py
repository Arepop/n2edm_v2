from PyQt5 import QtWidgets, QtCore, QtGui

from ..abstract.views import *


class BaseView(QtWidgets.QMainWindow, QtWidgets.QWidget, IBaseView):
    """BaseView class
    """
    def __init__(self):
        super(BaseView, self).__init__()
        self.setWindowTitle("n2EDM Scheduler v. 0.1.0")
        self.create_main_window()
        self.create_menu_bar()

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
        main_layout.addWidget(self.split_widget)
        
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

        self.undo_action = QtWidgets.QAction("Undo...")
        self.undo_action.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        self.redo_action = QtWidgets.QAction("Redo...")
        self.redo_action.setShortcut(QtGui.QKeySequence("Ctrl+Y"))

        self.edit_menu = main_menu.addMenu("Edit")
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)

        self.add_action = QtWidgets.QAction("Add Action...")

        self.add_timeline = QtWidgets.QAction("Add Timeline...")

        self.actions_menu = main_menu.addMenu("Actions")
        self.actions_menu.addAction(self.add_action)
        self.actions_menu.addAction(self.add_timeline)

class SchedulerView(QtWidgets.QWidget, ISchedulerView):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent=parent)
        self.create_canvas()
        self.set_canvas_attributes(100)
        self.set_canvas_labels()

    def create_canvas(self) -> None:
        """Create matplotlib canvas and tollbar
        """
        main_layout = QtWidgets.QVBoxLayout(self)

        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)

    def update_canvas(self):
        for actor in ActorObject.all():
            self.canvas.draw()

    def set_canvas_attributes(self, Y_MAX) -> None:
        """Sets canvas attributes
        """
        bbox = self.ax.get_window_extent().transformed(
            self.figure.dpi_scale_trans.inverted())
        WIDTH = 2 * bbox.height

        mpl.rcParams["lines.solid_capstyle"] = "butt"
        self.ax.grid(True)
        self.ax.set_xbound(0)
        self.ax.set_ylim(25, -1)
        self.ax.set_xlim(-1, 200)
        plt.yticks(range(-2, 25))
        self.set_canvas_labels()

    def set_canvas_labels(self) -> None:
        self.ax.set_yticklabels(["", "Timeline"]+[""]*25)
        self.figure.tight_layout()
        self.canvas.draw()

class SearchBarView(QtWidgets.QLineEdit, ISearchBarView):
    """Constructor for overwritten QLineEdit

    Args:
        QtWidgets (QWidget): QLineEdit
    """

    search_sig = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__(parent)

    def keyPressEvent(self, event: QtCore.QEvent) -> None:
        """Send string as signal to tree_view to search signals in tree_view

        Args:
            event (QEvent): Pressed key event
        """
        super().keyPressEvent(event)
        if event.key():
            self.search_sig.emit(self.text())

class TreeView(QtWidgets.QWidget, ITreeView)
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)

class ActionsView(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)