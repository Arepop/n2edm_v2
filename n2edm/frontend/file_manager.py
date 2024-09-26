import libconf
from typing import Any

from .dialogs import CycleDefine
from ..api import SetAPI, GroupAPI, ScheduleAPI, SequencerAPI

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog

SCHEDULE_API = ScheduleAPI()
SET_API = SetAPI()
GROUP_API = GroupAPI()
SEQUENCER_API = SequencerAPI()


class FileManager(QWidget):
    set_items_loaded_event = pyqtSignal(list, list)
    schedule_loaded_event = pyqtSignal(list)

    def __init__(self, parent) -> None:
        self.parent = parent
        self.q_file_dialog = None
        super().__init__(parent)

    def load_set_items(self):
        """Loads action from file"""
        options = QFileDialog.Options()
        self.q_file_dialog, _ = QFileDialog.getOpenFileName(
            self.parent,
            "QFileDialog.getOpenFileName()",
            "",
            "Tree Files (*.tree);;All Files (*)",
            options=options,
        )
        if not self.q_file_dialog:
            return
        with open(self.q_file_dialog, "r") as file:
            data = libconf.load(file)
        groups, set_items = self.deserialize(data)
        self.set_items_loaded_event.emit(groups, set_items)

    def save_set_items(self):
        """Saves actions to file"""
        set_items = SET_API.get_all_items()
        group_items = GROUP_API.get_all_items()
        data = self.serialize(set_items, group_items)
        options = QFileDialog.Options()
        self.q_file_dialog, extensions = QFileDialog.getSaveFileName(
            self.parent,
            "QFileDialog.getSaveFileName()",
            "",
            "Tree Files (*.tree);;All Files (*)",
            options=options,
        )
        if "tree" in extensions and "tree" not in self.q_file_dialog:
            self.q_file_dialog += ".tree"
        if not self.q_file_dialog:
            return
        with open(self.q_file_dialog, "w") as file:
            libconf.dump(data, file)

    def load_schedule(self):
        """Loads action from file"""
        options = QFileDialog.Options()
        self.q_file_dialog, _ = QFileDialog.getOpenFileName(
            self.parent,
            "QFileDialog.getOpenFileName()",
            "",
            "Tree Files (*.schedule);;All Files (*)",
            options=options,
        )
        if not self.q_file_dialog:
            return
        with open(self.q_file_dialog, "r") as file:
            data = libconf.load(file)
        items = self.deserialize_schedule(data)
        self.schedule_loaded_event.emit(items)

    def save_schedule(self):
        """Saves schedule to file"""
        schedule_items = SCHEDULE_API.get_all_items()
        data = self.serialize_schedule(schedule_items)
        options = QFileDialog.Options()
        self.q_file_dialog, extensions = QFileDialog.getSaveFileName(
            self.parent,
            "QFileDialog.getSaveFileName()",
            "",
            "Tree Files (*.schedule);;All Files (*)",
            options=options,
        )
        if "schedule" in extensions:
            self.q_file_dialog += ".schedule"
        if not self.q_file_dialog:
            return
        with open(self.q_file_dialog, "w") as file:
            libconf.dump(data, file)

    def serialize_schedule(self, schedule_items: list):
        data = {}
        for item in schedule_items:
            item_as_dict: dict = self.replace_none(item.as_dict())
            item_as_dict["set_item"] = item.set_item.uid
            data[f"I{item.uid}"] = item_as_dict
        return data

    def deserialize_schedule(self, data: dict):
        items = [self.replace_null(value) for value in data.values()]
        return items

    def serialize(self, set_items: list, group_items: list) -> dict:
        data = {}
        for group_item in group_items:
            item_as_dict: dict = self.replace_none(group_item.as_dict())
            data[f"G{group_item.uid}"] = item_as_dict

        for set_item in set_items:
            item_as_dict = self.replace_none(set_item.as_dict())
            if set_item.group_item:
                item_as_dict["group_item"] = set_item.group_item.uid
            data[f"S{set_item.uid}"] = item_as_dict

        return data

    def deserialize(self, data: dict) -> tuple:
        groups = [self.replace_null(value) for key, value in data.items() if "G" in key]
        set_items = [self.replace_null(value) for key, value in data.items() if "S" in key]
        return groups, set_items

    def replace_none(self, item_dict: dict) -> dict:
        return {key: value if value is not None else "null" for key, value in item_dict.items()}

    def replace_null(self, item_dict: dict) -> dict:
        return {key: value if value != "null" else None for key, value in item_dict.items()}

    def save_sequence(self):
        sequence = SEQUENCER_API.get_sequence()
        options = QFileDialog.Options()
        self.q_file_dialog, extensions = QFileDialog.getSaveFileName(
            self.parent,
            "QFileDialog.getSaveFileName()",
            "",
            "All Files (*)",
            options=options,
        )
        if not self.q_file_dialog:
            return
        with open(self.q_file_dialog, "w") as file:
            file.writelines(sequence)

    def set_number_of_cycles(self):
        number_of_cycles = SEQUENCER_API.get_number_of_cycles()
        cycle_dialog = CycleDefine(self, number_of_cycles)
        cycle_dialog.exec()
        number_of_cycles = cycle_dialog.number
        SEQUENCER_API.set_number_of_cycles(number_of_cycles)
