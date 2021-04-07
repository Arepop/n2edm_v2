from typing import Any

from PyQt5 import QtWidgets, QtCore, QtGui


class BaseView(QtWidgets.QMainWindow, QtWidgets.QWidget):
    """BaseView class
    """
    def __init__(self):
        super(BaseView, self).__init__()
        self.setWindowTitle("n2EDM Scheduler v. 0.1.0")
        self.create_main_window()

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


class SchedulerView(QtWidgets.QWidget):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
class SearchBarView(QtWidgets.QLineEdit):
    """Constructor for overwritten QLineEdit

    Args:
        QtWidgets (QWidget): QLineEdit
    """
    def __init__(self, parent):
        super().__init__(parent)


class TreeView(QtWidgets.QTreeView):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)


class ActionsView(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout(self)
