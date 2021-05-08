from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal as Signal

from .helpers import colorQPushButton

class CoreDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)


class ActionDialog(CoreDialog):
    """ActionWizzard class. Dialog window to define action for schedule.

    Args:
        parent (QWidget): parent widget of dialog

    Attributes:
        self.group_name (str): Group name for action.
        self.action_name: (str): Action name
        self.start (int): Start SCPI command
        self.stop (int): Stop SCPI command
        self.parameter (str): Additional parameters to command
        self.time_distance (int): Base time distance (duration) of action
        self.color (str): colour of action as hex
        self.temp_names (list): List of temporary reserved names for groups
    """

    SIG_create_action = Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Create Action")
        self.resize(640, 100)
        self.init_layout()
        self.init_widgets()
        self.connections()
        
        self.group = None
        self.name = None
        self.start_cmd = None
        self.stop_cmd = None
        self.params = None
        self.duration = None
        self.color = None

        self.attr = ['group', 'name', 'start_cmd', 'stop_cmd', 'params', 'duration', 'color']

    def init_layout(self) -> None:
        """Initiate all layout for dialog

        Returns:
            None
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.group_line_layout = QtWidgets.QHBoxLayout()
        self.action_line_layout = QtWidgets.QHBoxLayout()
        self.start_cmd_line_layout = QtWidgets.QHBoxLayout()
        self.stop_cmd_line_layout = QtWidgets.QHBoxLayout()
        self.time_distance_line_layout = QtWidgets.QHBoxLayout()
        self.parameter_line_layout = QtWidgets.QHBoxLayout()
        self.color_line_layout = QtWidgets.QHBoxLayout()
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.group_line_layout)
        self.layout.addLayout(self.action_line_layout)
        self.layout.addLayout(self.start_cmd_line_layout)
        self.layout.addLayout(self.stop_cmd_line_layout)
        self.layout.addLayout(self.time_distance_line_layout)
        self.layout.addLayout(self.parameter_line_layout)
        self.layout.addLayout(self.color_line_layout)
        self.layout.addLayout(self.button_line_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def init_widgets(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        self.group_label = QtWidgets.QLabel("Chose Group")
        self.group_combo_box = QtWidgets.QComboBox()
        self.group_combo_box.setSizePolicy(
            Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        self.group_line_layout.addWidget(self.group_label)
        self.group_line_layout.addWidget(self.group_combo_box)
        self.action_label = QtWidgets.QLabel("Name Action")
        self.action_name_line = QtWidgets.QLineEdit()
        self.action_line_layout.addWidget(self.action_label)
        self.action_line_layout.addWidget(self.action_name_line)
        self.start_label = QtWidgets.QLabel("Start SCPI")
        self.start_line = QtWidgets.QLineEdit()
        self.start_cmd_line_layout.addWidget(self.start_label)
        self.start_cmd_line_layout.addWidget(self.start_line)
        self.stop_label = QtWidgets.QLabel("Stop SCPI")
        self.stop_line = QtWidgets.QLineEdit()
        self.stop_cmd_line_layout.addWidget(self.stop_label)
        self.stop_cmd_line_layout.addWidget(self.stop_line)
        self.time_distance_label = QtWidgets.QLabel("Time Distance")
        self.time_distance_line = QtWidgets.QLineEdit()
        self.time_distance_line_layout.addWidget(self.time_distance_label)
        self.time_distance_line_layout.addWidget(self.time_distance_line)
        self.parameter_label = QtWidgets.QLabel("Parameter")
        self.parameter_line = QtWidgets.QLineEdit()
        self.parameter_line_layout.addWidget(self.parameter_label)
        self.parameter_line_layout.addWidget(self.parameter_line)
        self.color_label = QtWidgets.QLabel("color")
        self.color_button = colorQPushButton("Set")
        self.color_button.setSizePolicy(
            Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        self.color_line_layout.addWidget(self.color_label)
        self.color_line_layout.addWidget(self.color_button)
        self.confirm_button = QtWidgets.QPushButton("Create")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)
        self.status_bar = QtWidgets.QStatusBar()
        self.layout.addWidget(self.status_bar)

    def connections(self) -> None:
        """Connects all used slots and signals

        Returns:
            None
        """
        self.cancel_button.clicked.connect(self.cancel)
        self.confirm_button.clicked.connect(self.set_action_data)

    def fill_group_combo_box(self, groups=[]) -> None:
        """After loading widgets GroupComboBox is filled with existing group names
        """
        self.group_combo_box.addItem("...", None)
        self.group_combo_box.addItem("Create...", "...")
        for group in groups:
            self.group_combo_box.addItem(group.name, group)


    def set_action_data(self) -> None:
        """Reads action attributes and data from text fields and assign them with
        uniqe ID for every action. Next data is emmited in signal.
        """
        self.group = self.group_combo_box.currentData()
        self.name = self.action_name_line.text()
        self.start_cmd = self.start_line.text()
        self.stop_cmd = self.stop_line.text()
        self.duration = int(self.time_distance_line.text())
        self.params = self.parameter_line.text()
        self.color = self.color_button.color()
        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr) if getattr(self, attr) != "" else None
        self.SIG_create_action.emit(attributes)

    def cancel(self) -> None:
        """After clicking close button dialog is closes.
        """
        self.close()


class EditActionDialog(ActionDialog):

    SIG_edit_action = Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget, action) -> None:
        super().__init__(parent)
        self.setWindowTitle("Update Action")
        self.confirm_button.setText('Update')
        self.action = action
        self.action_name_line.setText(self.action.name)
        self.start_line.setText(self.action.start_cmd) 
        self.stop_line.setText(self.action.stop_cmd)
        self.time_distance_line.setText(str(self.action.duration)) 
        self.parameter_line.setText(self.action.params)
        self.color_button.set_color(self.action.color)
        self.confirm_button.clicked.connect(self.set_edit_data)

    def fill_group_combo_box(self, groups=[]):
        super().fill_group_combo_box(groups=groups)
        if self.action.group:
            self.group_combo_box.setCurrentText(self.action.group.name)

    def set_edit_data(self) -> None:
        """Reads action attributes and data from text fields and assign them with
        uniqe ID for every action. Next data is emmited in signal.
        """
        self.group = self.group_combo_box.currentData()
        self.name = self.action_name_line.text()
        self.start_cmd = self.start_line.text()
        self.stop_cmd = self.stop_line.text()
        self.duration = int(self.time_distance_line.text())
        self.params = self.parameter_line.text()
        self.color = self.color_button.color()
        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr)
        self.SIG_edit_action.emit(attributes)
        self.close()

class GroupDialog(CoreDialog):
    """GroupWizzard class. Dialog opens when user choses to create new group for actions.

    Args:
        parent (QWidget): parent widget of dialog
        tree (QTreeView): tree with defined actions and groups
    """

    SIG_create_group = Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Create Group")
        self.init_layout()
        self.init_widgets()
        self.connections()
        self.resize(300, 50)

        self.attr = ['name']


    def init_layout(self) -> None:
        """Initiate all layout for dialog

        Returns:
            None
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.group_line_layout = QtWidgets.QHBoxLayout()
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.group_line_layout)
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        self.group_label = QtWidgets.QLabel("Chose Group")
        self.group_name_line = QtWidgets.QLineEdit()
        self.group_line_layout.addWidget(self.group_label)
        self.group_line_layout.addWidget(self.group_name_line)
        self.confirm_button = QtWidgets.QPushButton("Create")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)
        self.status_bar = QtWidgets.QStatusBar()
        self.layout.addWidget(self.status_bar)

    def connections(self) -> None:
        """Connects all used slots and signals

        Returns:
            None
        """
        self.confirm_button.clicked.connect(self.set_group_data)
        self.cancel_button.clicked.connect(self.cancel)

    def set_group_data(self) -> None:
        """Reads action attributes and data from text fields and assign them with
        uniqe ID for every action. Next data is emmited in signal.
        """
        self.name = self.group_name_line.text()

        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr)
        self.SIG_create_group.emit(attributes)
        self.close()

    def cancel(self) -> None:
        """After clicking close button dialog closes.
        """
        self.close()

class ErrorDialog(CoreDialog):
    def __init__(self, exctype, value, traceback, traceback_string):
        super().__init__(None)
        self.resize(200, 50)
        self.exectype = exctype
        self.value = value
        self.traceback = traceback
        self.traceback_string = traceback_string

        self.layout = QtWidgets.QVBoxLayout()
        self.error_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.error_layout)
        self.layout.addLayout(self.button_layout)
        self.error_label = QtWidgets.QLabel(str(self.exectype))
        self.error_info_label = QtWidgets.QLabel(str(self.value))
        self.error_button = QtWidgets.QPushButton("Ok")

        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.error_info_label)
        self.layout.addWidget(self.error_button)
        self.error_button.clicked.connect(lambda: self.close())
        self.setLayout(self.layout)

    def traceback(self):
        return self.traceback


class DiffDialog(CoreDialog):
    def __init__(self, obj, attributes):
        super().__init__(self)
        # self.resize(200, 50)

    def init_layout(self) -> None:
        """Initiate all layout for dialog

        Returns:
            None
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        self.scroll_area = QtWidgets.QScrollArea()
        self.tree_view = QtWidgets.QTreeWidget()        
        self.confirm_button = QtWidgets.QPushButton("Create")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)
        self.status_bar = QtWidgets.QStatusBar()
        self.layout.addWidget(self.status_bar)

    def check_differences(self, obj, attributes):
        pass

    def next_diff(self, iter):
        pass

    def prev_diff(self, iter):
        pass

    def select_diff(self, diff_line):
        pass

