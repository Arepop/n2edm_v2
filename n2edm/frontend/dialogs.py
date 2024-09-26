from PyQt5 import Qt, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal

from .helpers import colorQPushButton

# import .global_


class CreateSetItemDialog(QtWidgets.QDialog):
    """CreateSetItemDialog window. Dialog window to define set_item for schedule.

    Args:
        parent (QWidget): parent widget of dialog

    Attributes:
        self.group_name (str): Group name for set_item.
        self.action_name: (str): Action name
        self.start (int): Start SCPI command
        self.stop (int): Stop SCPI command
        self.parameter (str): Additional parameters to command
        self.time_distance (int): Base time distance (duration) of set_item
        self.color (str): colour of set_item as hex
        self.temp_names (list): List of temporary reserved names for groups
    """

    create_set_item_event = Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget, set_item) -> None:
        super().__init__(parent)
        self.parent = parent
        self.set_item = set_item
        self.setWindowTitle("Create Action")
        self.resize(640, 100)
        self.init_layout()
        self.init_widgets()
        self.connections()

        self.group_item = None
        self.name = None
        self.initial_scpi_command = None
        self.final_scpi_command = None
        self.params = None
        self.duration = None
        self.color = None

        self.attr = [
            "group_item",
            "name",
            "initial_scpi_command",
            "final_scpi_command",
            "params",
            "duration",
            "color",
        ]

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
        self.group_combo_box.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
        self.group_line_layout.addWidget(self.group_label)
        self.group_line_layout.addWidget(self.group_combo_box)
        self.action_label = QtWidgets.QLabel("Name Action")
        self.set_item_name_line = QtWidgets.QLineEdit()
        self.action_line_layout.addWidget(self.action_label)
        self.action_line_layout.addWidget(self.set_item_name_line)
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
        self.time_distance_line.setValidator(QtGui.QIntValidator(0, 100000))
        self.parameter_label = QtWidgets.QLabel("Parameter")
        self.parameter_line = QtWidgets.QLineEdit()
        self.parameter_line_layout.addWidget(self.parameter_label)
        self.parameter_line_layout.addWidget(self.parameter_line)
        self.color_label = QtWidgets.QLabel("color")
        self.color_button = colorQPushButton("Set")
        self.color_button.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum)
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
        self.time_distance_line.textEdited.connect(self.additional_validate)

    def additional_validate(self, text):
        if len(text) > 5:
            text = text[1:]
            self.time_distance_line.setText(text)
        try:
            int(text)
        except ValueError:
            self.time_distance_line.setText(text[:-1])

    def fill_group_combo_box(self, groups=[]) -> None:
        """After loading widgets GroupComboBox is filled with existing group_item names"""
        self.group_combo_box.addItem("...", None)
        self.group_combo_box.addItem("Create...", "...")
        for group_item in groups:
            self.group_combo_box.addItem(group_item.name, group_item.uid)

        if hasattr(self.set_item, "group_item"):
            if self.set_item.group_item != None:
                self.group_combo_box.setCurrentText(self.set_item.group_item.name)
        elif hasattr(self.set_item, "name"):
            self.group_combo_box.setCurrentText(self.set_item.name)

    def set_action_data(self) -> None:
        """Reads set_item attributes and data from text fields and assign them with
        uniqe ID for every set_item. Next data is emmited in signal.
        """
        self.group_item = self.group_combo_box.currentData()
        self.name = self.set_item_name_line.text()
        self.initial_scpi_command = self.start_line.text()
        self.final_scpi_command = self.stop_line.text()
        try:
            self.duration = int(self.time_distance_line.text())
        except ValueError as e:
            self.duration = 0
        self.params = self.parameter_line.text()
        self.color = self.color_button.color()
        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr) if getattr(self, attr) != "" else None
        self.create_set_item_event.emit(attributes)

    def cancel(self) -> None:
        """After clicking close button dialog closes."""
        self.close()


class EditSetItemDialog(CreateSetItemDialog):

    update_set_item_event = Signal(object, dict)

    def __init__(self, parent: QtWidgets.QWidget, set_item) -> None:
        super().__init__(parent, set_item)
        self.setWindowTitle("Update Action")
        self.confirm_button.setText("Update")
        self.set_item = set_item
        self.set_item_name_line.setText(self.set_item.name)
        self.start_line.setText(self.set_item.initial_scpi_command)
        self.stop_line.setText(self.set_item.final_scpi_command)
        self.time_distance_line.setText(str(self.set_item.duration))
        self.parameter_line.setText(self.set_item.params)
        self.color_button.set_color(self.set_item.color)
        self.confirm_button.clicked.connect(self.set_update_data)

    def set_update_data(self) -> None:
        """Reads set_item attributes and data from text fields and assign them with
        uniqe ID for every set_item. Next data is emmited in signal.
        """
        self.group_item = self.group_combo_box.currentData()
        self.name = self.set_item_name_line.text()
        self.initial_scpi_command = self.start_line.text()
        self.final_scpi_command = self.stop_line.text()
        self.duration = int(self.time_distance_line.text())
        self.params = self.parameter_line.text()
        self.color = self.color_button.color()
        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr)
        self.update_set_item_event.emit(self.set_item, attributes)
        self.close()


class CreateGroupDialog(QtWidgets.QDialog):
    """GroupWizzard class. Dialog opens when user choses to create new group_item for actions.

    Args:
        parent (QWidget): parent widget of dialog
        tree (QTreeView): tree with defined actions and groups
    """

    create_group_item_event = Signal(dict)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Create Group")
        self.init_layout()
        self.init_widgets()
        self.connections()
        self.resize(300, 50)

        self.attr = ["name"]

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
        self.confirm_button.clicked.connect(self.set_group_item_data)
        self.cancel_button.clicked.connect(self.cancel)

    def set_group_item_data(self) -> None:
        """Reads set_item attributes and data from text fields and assign them with
        uniqe ID for every set_item. Next data is emmited in signal.
        """
        self.name = self.group_name_line.text()

        attributes = {}
        for attr in self.attr:
            attributes[attr] = getattr(self, attr)
        self.create_group_item_event.emit(attributes)
        self.close()

    def cancel(self) -> None:
        """After clicking close button dialog closes."""
        self.close()


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, exctype, value, traceback, traceback_string):
        super().__init__(None)
        self.resize(200, 50)
        self.exectype = exctype
        self.value = value
        self.traceback_ = traceback
        self.traceback_string = traceback_string
        self.setWindowTitle("An error has occured!")

        self.layout = QtWidgets.QVBoxLayout()
        self.error_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.error_layout)
        self.layout.addLayout(self.button_layout)
        self.error_info_label = QtWidgets.QLabel(str(self.value))
        self.error_button = QtWidgets.QPushButton("Ok")

        self.layout.addWidget(self.error_info_label)
        self.layout.addWidget(self.error_button)
        self.error_button.clicked.connect(lambda: self.close())
        self.setLayout(self.layout)

    def traceback(self):
        return self.traceback_


class ScheduleItemCreateDialog(QtWidgets.QDialog):
    """ScheduleItemCreate dialog. After doubleclicking on ScheduleItem or creating it, dialog with time settings appears.

    Args:
        set_item (SetItem): clicked actor
    """

    def __init__(self, parent, set_item: object) -> None:
        super().__init__(parent)
        self.set_item = set_item
        self.init_layout()
        self.init_widgets()
        self.connections()
        self.closed = False
        self.setWindowTitle(f"Set time for: {self.set_item.name}")
        self.attributes = {"start": 0, "stop": 0, "sequence": "main", "continuous": False}
        self.read_values()

    def init_layout(self) -> None:
        """Initiate all layout for dialog

        Returns:
            None
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.sequence_layout = QtWidgets.QHBoxLayout()
        self.sequence_vlayout = QtWidgets.QVBoxLayout()
        self.start_layout = QtWidgets.QHBoxLayout()
        self.stop_layout = QtWidgets.QHBoxLayout()
        self.time_distance_layout = QtWidgets.QHBoxLayout()
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.sequence_layout.addLayout(self.sequence_vlayout)
        self.layout.addLayout(self.start_layout)
        self.layout.addLayout(self.stop_layout)
        self.layout.addLayout(self.time_distance_layout)
        self.layout.addLayout(self.sequence_layout)
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        self.sequence_label = QtWidgets.QLabel("Actor sequence")
        self.sequence_buttons = {
            "pre": QtWidgets.QRadioButton("Preambule"),
            "main": QtWidgets.QRadioButton("Cycle"),
            "post": QtWidgets.QRadioButton("Coda"),
        }
        self.sequence_buttons["main"].setChecked(True)
        self.sequence_layout.addWidget(self.sequence_label)
        for button in self.sequence_buttons.values():
            self.sequence_layout.addWidget(button)
        self.start_label = QtWidgets.QLabel("Start time")
        self.start_line = QtWidgets.QLineEdit()
        self.start_layout.addWidget(self.start_label)
        self.start_layout.addWidget(self.start_line)
        self.stop_label = QtWidgets.QLabel("Stop time")
        self.stop_line = QtWidgets.QLineEdit()
        self.stop_layout.addWidget(self.stop_label)
        self.stop_layout.addWidget(self.stop_line)
        self.time_distance_label = QtWidgets.QLabel("Time Distance")
        self.time_distance_line = QtWidgets.QLineEdit()
        self.time_distance_layout.addWidget(self.time_distance_label)
        self.time_distance_layout.addWidget(self.time_distance_line)
        self.start_line.setValidator(QtGui.QIntValidator(0, 10000))
        self.stop_line.setValidator(QtGui.QIntValidator())
        self.time_distance_line.setValidator(QtGui.QIntValidator())
        self.confirm_button = QtWidgets.QPushButton("Ok")
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
        self.confirm_button.clicked.connect(self.set_time)
        self.cancel_button.clicked.connect(self.cancel)
        self.stop_line.textEdited.connect(self.set_duration_time)
        self.start_line.textEdited.connect(self.set_stop_time)
        self.time_distance_line.textEdited.connect(self.set_stop_time)

    def cancel(self) -> None:
        """Closes dialog"""
        self.closed = True
        self.close()

    def set_duration_time(self, time: str) -> None:
        """Calculate and sets absolute difference between start and stop
        time when not in edition state.

        Args:
            time (str): slot for text from start and stop fields signals
        """
        if self.stop_line.text() == "" or self.start_line.text() == "":
            return
        time_distance_line = abs(int(self.stop_line.text()) - int(self.start_line.text()))
        self.time_distance_line.setText(str(time_distance_line))

    def set_stop_time(self, time: str) -> None:
        """Calculate and sets stop time based on start and time_distance text fields
        when not in edition state.

        Args:
            time (str): slot for text from start and stop fields signals. Exeption when empty.
        """

        if time == "" or self.start_line.text() == "":
            return
        stop_time = abs(int(self.start_line.text()) + int(self.time_distance_line.text()))
        self.stop_line.setText(str(stop_time))

    def set_time(self):
        """Reads all values from text fields. Update time for actor and handles infinity actors.
        Handles errors in time flow.
        """
        self.attributes["start"] = int(self.start_line.text())
        if self.attributes["stop"] != None:
            self.attributes["stop"] = int(self.stop_line.text())
        for sequence, button in self.sequence_buttons.items():
            if button.isChecked():
                self.attributes["sequence"] = sequence
                break
        # self.attributes["execution_time"] = float(self.execution_line.text())

        self.close()

    def read_values(self) -> None:
        """Reads start and stop positions of actor to initially fill text fields"""
        self.start_line.setText(str(self.attributes["start"]))
        if self.attributes["continuous"]:
            self.stop_line.setEnabled(False)
            self.time_distance_line.setEnabled(False)
            self.stop_line.setText(str(0))
            self.time_distance_line.setText(str(0))
        else:
            self.stop_line.setText(str(self.attributes["stop"]))
            self.time_distance_line.setText(
                str(self.attributes["stop"] - self.attributes["start"])
            )


class ScheduleItemEditDialog(ScheduleItemCreateDialog):
    """ScheduleItemCreate dialog. After doubleclicking on ScheduleItem or creating it, dialog with time settings appears.

    Args:
        set_item (SetItem): clicked actor
    """

    update_schedule_item_event = Signal(object, dict)

    def __init__(self, parent, schedule_item: object) -> None:
        self.schedule_item = schedule_item
        super().__init__(parent, schedule_item.set_item)
        self.set_dialog_values()

    def set_dialog_values(self):
        self.start_line.setText(str(self.schedule_item.start_time))
        self.stop_line.setText(str(self.schedule_item.stop_time))
        time_distance_line = abs(int(self.stop_line.text()) - int(self.start_line.text()))
        self.time_distance_line.setText(str(time_distance_line))

    def connections(self) -> None:
        """Connects all used slots and signals

        Returns:
            None
        """
        self.confirm_button.clicked.connect(self.set_time)
        self.cancel_button.clicked.connect(self.cancel)
        self.stop_line.textEdited.connect(self.set_duration_time)
        self.start_line.textEdited.connect(self.set_stop_time)
        self.time_distance_line.textEdited.connect(self.set_stop_time)


class CycleDefine(QtWidgets.QDialog):

    def __init__(self, parent, number=0):
        super().__init__(parent)
        self.number = number
        self.init_layout()
        self.init_widgets()
        self.connections()

    def init_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.cycle_number_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.cycle_number_layout)
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self):
        self.number_label = QtWidgets.QLabel("No. cycles")
        self.number_input = QtWidgets.QLineEdit(str(self.number))
        self.number_input.setValidator(QtGui.QIntValidator())
        self.confirm_button = QtWidgets.QPushButton("Ok")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)

        self.cycle_number_layout.addWidget(self.number_label)
        self.cycle_number_layout.addWidget(self.number_input)

    def connections(self) -> None:
        """Connects all used slots and signals

        Returns:
            None
        """
        self.confirm_button.clicked.connect(self.set_cycle_number)
        self.cancel_button.clicked.connect(self.cancel)

    def set_cycle_number(self):
        self.number = int(self.number_input.text())
        # self.SIG_number_of_cycles.emit(int(self.number))
        self.close()

    def cancel(self) -> None:
        """Closes dialog"""
        self.close()


class DBPushDialog(QtWidgets.QDialog):

    SIG_push_to_db = Signal(str, str)

    def __init__(self, parent: QtWidgets.QWidget, set_name, schedule_name) -> None:
        super().__init__(parent)
        self.set_name = set_name
        self.schedule_name = schedule_name
        self.init_layout()
        self.init_widgets()
        self.connections()

    def init_layout(self):
        """Initialze layout for DBPush window"""
        self.layout = QtWidgets.QVBoxLayout()
        self.set_name_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.set_name_layout)
        self.schedule_name_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.schedule_name_layout)
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self):
        """Initialize widgets inside window"""
        self.set_name_label = QtWidgets.QLabel("Set name")
        self.set_name_text = QtWidgets.QLineEdit()
        if self.set_name:
            self.set_name_text.setText(self.set_name)
        self.schedule_name_label = QtWidgets.QLabel("Schedule name")
        self.schedule_name_text = QtWidgets.QLineEdit()
        if self.schedule_name:
            self.schedule_name_text.setText(self.schedule_name)
        self.confirm_button = QtWidgets.QPushButton("Push")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.set_name_layout.addWidget(self.set_name_label)
        self.set_name_layout.addWidget(self.set_name_text)
        self.schedule_name_layout.addWidget(self.schedule_name_label)
        self.schedule_name_layout.addWidget(self.schedule_name_text)
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)

    def connections(self):
        """Connect signals and slots"""
        self.confirm_button.clicked.connect(self.push_to_db)
        self.cancel_button.clicked.connect(self.cancel)

    def push_to_db(self):
        """Pushes data do database"""
        set_name = self.set_name_text.text()
        schedule_name = self.schedule_name_text.text()
        self.SIG_push_to_db.emit(set_name, schedule_name)
        self.close()

    def cancel(self) -> None:
        """Closes dialog"""
        self.close()


class DBPullDialog(QtWidgets.QDialog):

    SIG_set_selected = Signal(str)
    SIG_pull_requested = Signal(str, str)

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.init_layout()
        self.init_widgets()
        self.set_selected_text = None
        self.schedule_selected_text = None
        self.set_list_widget.itemClicked.connect(self.set_selected)
        self.schedule_list_widget.itemClicked.connect(self.schedule_selected)
        self.confirm_button.clicked.connect(self.pull_from_db)
        self.cancel_button.clicked.connect(self.cancel)

    def init_layout(self) -> None:
        """Initiate all layout for dialog

        Returns:
            None
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.set_list_layout = QtWidgets.QVBoxLayout()
        self.schedule_list_layout = QtWidgets.QVBoxLayout()
        self.button_line_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.set_list_layout)
        self.layout.addLayout(self.schedule_list_layout)
        self.layout.addLayout(self.button_line_layout)
        self.setLayout(self.layout)

    def init_widgets(self) -> None:
        """Initiate all main widgets in main window

        Returns:
            None
        """
        self.set_list_widget = QtWidgets.QListWidget()
        self.schedule_list_widget = QtWidgets.QListWidget()
        self.confirm_button = QtWidgets.QPushButton("Pull")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_line_layout.addWidget(self.confirm_button)
        self.button_line_layout.addWidget(self.cancel_button)
        self.set_list_layout.addWidget(self.set_list_widget)
        self.schedule_list_layout.addWidget(self.schedule_list_widget)

    def fill_set_list(self, qs: list):
        """Fills list with set names

        Args:
            qs (list): listlike of set names
        """
        for item in list(qs):
            self.set_list_widget.addItem(item["set_name"])

    def fill_schedule_list(self, qs: list):
        """Fills list with schedule names

        Args:
            qs (list): listlike of schedule names
        """
        self.schedule_list_widget.clear()
        for item in list(qs):
            self.schedule_list_widget.addItem(item)

    def set_selected(self, list_item: str):
        """Set current set

        Args:
            list_item (str): item to be set from db
        """
        self.SIG_set_selected.emit(list_item.text())
        self.set_selected_text = list_item.text()

    def schedule_selected(self, list_item: str):
        """Set current schedule

        Args:
            list_item (str): item to be set from db
        """
        self.schedule_selected_text = list_item.text()

    def pull_from_db(self):
        """Pulls selected set and schuule from database"""
        self.SIG_pull_requested.emit(self.set_selected_text, self.schedule_selected_text)
        self.close()

    def cancel(self) -> None:
        """Closes dialog"""
        self.close()


# class TimelineCreationDialog(QtWidgets.QDialog):

#     SIG_timeline_object_created = Signal(object)

#     def __init__(self, parent: QtWidgets.QWidget, attributes=None):
#         super().__init__(parent)
#         self.attributes = attributes if attributes else {}
#         self.edit = False
#         self.closed = False
#         self.init_layout()
#         self.init_widgets()
#         self.fill_textfields(attributes)
#         self.cancel_button.clicked.connect(self.cancel)
#         self.confirm_button.clicked.connect(self.create_actor)

#     def init_layout(self):
#         """Initiate all layout for dialog

#         Returns:
#             None
#         """
#         self.layout = QtWidgets.QVBoxLayout()
#         self.name_layout = QtWidgets.QHBoxLayout()
#         self.start_stop_layout = QtWidgets.QHBoxLayout()
#         self.color_layout = QtWidgets.QHBoxLayout()
#         self.buttons_layout = QtWidgets.QHBoxLayout()
#         self.layout.addLayout(self.name_layout)
#         self.layout.addLayout(self.start_stop_layout)
#         self.layout.addLayout(self.color_layout)
#         self.layout.addLayout(self.buttons_layout)

#         self.setLayout(self.layout)

#     def init_widgets(self):
#         self.name_label = QtWidgets.QLabel("Name")
#         self.name_textfield = QtWidgets.QLineEdit()
#         self.start_stop_label = QtWidgets.QLabel("Start/Stop")
#         self.start_textfield = QtWidgets.QLineEdit()
#         self.stop_textfield = QtWidgets.QLineEdit()
#         self.color_label = QtWidgets.QLabel("Color")
#         self.color_button = colorQPushButton("Set")

#         if self.attributes:
#             self.setWindowTitle("Update Timeline")
#             self.confirm_button = QtWidgets.QPushButton("Update")
#         else:
#             self.setWindowTitle("Create Timeline")
#             self.confirm_button = QtWidgets.QPushButton("Create")
#         self.cancel_button = QtWidgets.QPushButton("Cancel")

#         self.name_layout.addWidget(self.name_label)
#         self.name_layout.addWidget(self.name_textfield)

#         self.start_stop_layout.addWidget(self.start_stop_label)
#         self.start_stop_layout.addWidget(self.start_textfield)
#         self.start_stop_layout.addWidget(self.stop_textfield)
#         self.color_layout.addWidget(self.color_label)
#         self.color_layout.addWidget(self.color_button)
#         self.buttons_layout.addWidget(self.confirm_button)
#         self.buttons_layout.addWidget(self.cancel_button)

#     def create_actor(self):
#         self.attributes["name"] = self.name_textfield.text()
#         if self.stop_textfield.text() == "":
#              STOP.showMessage()
#         self.attributes["start"] = float(self.start_textfield.text())
#         self.attributes["stop"] = float(self.stop_textfield.text())
#         .global_.TimeLineStop = float(self.stop_textfield.text())
#         self.attributes["color"] = self.color_button.color()
#         self.attributes["annotate"] = self.name_textfield.text()
#         self.attributes["text"] = self.name_textfield.text()
#         .global_.TimeLineText = self.name_textfield.text()
#         self.attributes["position"] = -1
#         if .global_.TimeLineEdit == 0:
#             self.start_textfield.setText(str(.global_.TimeLineStop))
#         self.name_textfield.setText(.global_.TimeLineText)
#         if self.edit:
#             self.SIG_timeline_object_created.emit(self.attributes)
#             """self.close()"""
#         else:
#             self.SIG_timeline_object_created.emit(self.attributes)

#     def fill_textfields(self, attributes):
#         self.name_textfield.setText(.global_.TimeLineText)
#         self.color_button.set_color('#ffbb33')
#         self.start_textfield.setText(str(.global_.TimeLineStop))
#         if not attributes:
#             return
#         self.start_textfield.setText(str(attributes["start"]))
#         self.stop_textfield.setText(str(attributes["stop"]))
#         self.color_button.set_color(attributes["color"])
#         self.edit = True

#     def cancel(self) -> None:
#         """After clicking close button dialog closes."""
#         self.close()
