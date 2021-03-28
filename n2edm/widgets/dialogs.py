from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal as Signal

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
        self.setWindowTitle("Add Action")
        self.resize(640, 100)
        self.init_layout()
        self.init_widgets()
        self.connections()
            
        self.group = None
        self.name = None
        self.start = None
        self.stop = None
        self.parameter = None
        self.distance = None
        self.color = None

        self.attr = ['group', 'name', 'start', 'stop', 'parameter', 'distance', 'color']

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
        self.confirm_button = QtWidgets.QPushButton("Add")
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

    def fill_group_combo_box(self) -> None:
        """After loading widgets GroupComboBox is filled with existing group names
        """
        self.group_combo_box.addItem("...", "...")
        self.group_combo_box.addItem("New...", "...")

    def set_action_data(self) -> None:
        """Reads action attributes and data from text fields and assign them with
        uniqe ID for every action. Next data is emmited in signal.
        """
        self.group = self.group_combo_box.currentText()
        self.name = self.action_name_line.text()
        self.start = self.start_line.text()
        self.stop = self.stop_line.text()
        self.distance = self.time_distance_line.text()
        self.parameter = self.parameter_line.text()
        self.color = self.color_button.color()
        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr)
        self.SIG_create_action.emit(attributes)

    def cancel(self) -> None:
        """After clicking close button dialog is closes.
        """
        self.close()


class colorQPushButton(QtWidgets.QPushButton):
    def __init__(self, name):
        super().__init__()
        self.rgba = "#000000"
        self.setStyleSheet("QPushButton {background-color:%s;}" % self.rgba)

    def mousePressEvent(self, event):
        self.q_color = QtWidgets.QColorDialog.getColor()
        self.rgba = self.q_color.name()
        self.setStyleSheet("QPushButton {background-color:%s;}" % self.rgba)

    def color(self):
        return self.rgba

    def set_color(self, color):
        self.rgba = color
        self.setStyleSheet("QPushButton {background-color:%s;}" % color)
