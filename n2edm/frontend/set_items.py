from typing import Any

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QAbstractItemView

from ..api import SetAPI, GroupAPI, BaseItemAPI
from .dialogs import CreateSetItemDialog, CreateGroupDialog, EditSetItemDialog
from ..backend.exceptions import ItemNotFoundException


SET_API = SetAPI()
GROUP_API = GroupAPI()
BASE_API = BaseItemAPI()


class SetItemsWindow(QtWidgets.QWidget):
    """QWidget connecting SetItemsTree and Searchbar in one window.

    Args:
        parent (QWigdet): MainWindow widget.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.create_widget()
        # self.setMaximumWidth(250)

    def create_widget(self) -> None:
        """Creates layout and widgets (Tree and Bar)"""
        self.search_bar = SearchBar(self)
        self.tree = SetItemsTree(self)
        self.search_bar.search_event.connect(self.tree.search)
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.tree)


class SearchBar(QtWidgets.QLineEdit):
    """Search bar for set_items"""

    search_event = Signal(str)

    def __init__(self, parent):
        super().__init__(parent=parent)

    def keyPressEvent(self, event: QtCore.QEvent) -> None:
        """Send string as signal to tree_view to search signals in tree_view

        Args:
            event (QEvent): Pressed key event
        """
        super().keyPressEvent(event)
        if event.key():
            self.search_event.emit(self.text())


class SetItemsTree(QtWidgets.QTreeView):

    create_schedule_item_event = Signal(object)
    set_item_updated_event = Signal(object)
    remove_item_event = Signal(object)
    set_items_tree_reloaded_event = Signal()

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)
        self.create_widget()

    def create_widget(self):
        """Create SetItemsTree widget (UI) and connects frontend models and logic."""
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.model = StandardItemModel(self)
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setRecursiveFilteringEnabled(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setModel(self.proxy_model)
        self.setDragDropMode(self.DragOnly)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.header().setStretchLastSection(False)

    def set_item_creation_dialog_combo_box_update(self, group_item):
        self.set_item_creation_dialog.group_combo_box.addItem(group_item.name, group_item.uid)
        self.set_item_creation_dialog.group_combo_box.setCurrentText(group_item.name)

    def create_set_item(self, set_item_data):
        set_item = SET_API.create_item(set_item_data)
        self.model.add_set_item(set_item)

    def create_group_item(self, group_item_data):
        group_item = GROUP_API.create_item(group_item_data)
        self.model.add_group_item(group_item)
        self.set_item_creation_dialog_combo_box_update(group_item)

    def bulk_create_items(self, group_items_data: list, set_items_data: list):
        self.model.clear()
        GROUP_API.clear()
        SET_API.clear()
        groups = GROUP_API.bulk_create_items(group_items_data)
        set_items = SET_API.bulk_create_items(set_items_data)
        for group in groups:
            self.model.add_group_item(group)
        for set_item in set_items:
            self.model.add_set_item(set_item)
        self.set_items_tree_reloaded_event.emit()

    def open_set_item_creation_dialog(self):
        """Opens and fills Action and Group create window"""
        obj = self.currentIndex().data(role=257)
        self.set_item_creation_dialog = CreateSetItemDialog(self, obj)
        self.setCurrentIndex(QtCore.QModelIndex())
        groups = GROUP_API.get_all_items()
        self.set_item_creation_dialog.fill_group_combo_box(groups)
        self.set_item_creation_dialog.create_set_item_event.connect(self.create_set_item)
        self.set_item_creation_dialog.group_combo_box.activated.connect(
            lambda: self.open_group_item_creation_dialog()
        )
        self.set_item_creation_dialog.exec()

    def open_group_item_creation_dialog(self):
        """Opens small window to write group_item name"""
        if self.set_item_creation_dialog.group_combo_box.currentText() == "Create...":
            group_dialog = CreateGroupDialog(self)
            group_dialog.create_group_item_event.connect(self.create_group_item)
            group_dialog.exec()

    def update_set_item(self, set_item, new_data):
        if new_data.get("group_item"):
            new_data["group_item"] = GROUP_API.get_item(new_data.get("group_item"))
        updated_item = SET_API.update_item(set_item.uid, new_data)

    def update_group_item(self, uid, new_data):
        updated_item = GROUP_API.update_item(uid, new_data)

    def open_update_item_dialog(self):
        data = self.currentIndex().siblingAtColumn(0).data(role=257)
        try:
            set_item = SET_API.get_item(data)
            self.open_set_item_update_dialog(set_item)
        except ItemNotFoundException:
            group_item = GROUP_API.get_item(data)
            self.open_group_item_update_dialog(group_item)

    def open_set_item_update_dialog(self, set_item):
        self.update_set_item_dialog = EditSetItemDialog(self, set_item)
        groups = GROUP_API.get_all_items()
        self.update_set_item_dialog.fill_group_combo_box(groups)
        self.update_set_item_dialog.update_set_item_event.connect(self.update_set_item)
        self.update_set_item_dialog.exec()
        source_index = self.proxy_model.mapToSource(self.currentIndex())
        standard_item = self.model.itemFromIndex(source_index)
        self.model.update_set_item(standard_item, set_item)
        self.set_item_updated_event.emit(set_item)

    def open_group_item_update_dialog(self):
        pass

    def remove_item(self):
        uid = self.currentIndex().siblingAtColumn(0).data(role=257)
        source_index = self.proxy_model.mapToSource(self.currentIndex())
        standard_item = self.model.itemFromIndex(source_index)
        item = BASE_API.get_item(uid=uid)
        self.remove_item_event.emit(item)
        self.model.remove_item(standard_item)
        BASE_API.remove_item(uid)

    def remove_group_item(self):
        pass

    def mouseDoubleClickEvent(self, event: QtCore.QEvent) -> None:
        """Overloaded method of mouseDoubleClickEvent. Emits signal with set_item (Adds actor).

        Args:
            event (QEvent): MouseClickEvent
        """
        set_item = self.currentIndex().data(role=257)
        if set_item is None:
            set_item = (
                self.currentIndex()
                .siblingAtColumn(self.currentIndex().column() - 1)
                .data(role=257)
            )

        try:
            set_item = SET_API.get_item(set_item)
        except ItemNotFoundException:
            return

        self.create_schedule_item_event.emit(set_item)

    def contextMenuEvent(self, event: QtCore.QEvent) -> None:
        """Context menu controller and looks for action tree.pardir

        Args:
            event (QtCore.QEvent): QContextEvent
        """
        self.menu = QtWidgets.QMenu(self)
        create_set_item_action = QtWidgets.QAction("Add Action", self)
        update_set_item_action = QtWidgets.QAction("Edit", self)
        remove_item_action = QtWidgets.QAction("Delete", self)
        create_set_item_action.triggered.connect(self.open_set_item_creation_dialog)
        update_set_item_action.triggered.connect(self.open_update_item_dialog)
        remove_item_action.triggered.connect(self.remove_item)
        self.menu.addAction(create_set_item_action)
        self.menu.addAction(update_set_item_action)
        self.menu.addAction(remove_item_action)
        self.menu.popup(QtGui.QCursor.pos())
        if not self.selectedIndexes():
            update_set_item_action.setEnabled(False)
            remove_item_action.setEnabled(False)

    def search(self, search_str: str) -> None:
        """Searches item in tree view by given name

        Args:
            search_str (str): Name of signal to seach
        """
        self.proxy_model.setFilterRegExp(search_str)


class StandardItemModel(QtGui.QStandardItemModel):
    """Model of items and data to hold by widget

    Args:
        parent (QWidget): parent widget

    Attributes:
        self.set_items (dict): dictionary with set_items
        self.groups (dict): dictionary with groups

    """

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(QtGui.QStandardItemModel, self).__init__()
        self.setColumnCount(2)
        self.parent = parent

    def add_group_item(self, group_item):
        item = QtGui.QStandardItem()
        item.setText(group_item.name)
        color_item = QtGui.QStandardItem()
        self.appendRow([item, color_item])
        item.setData(group_item.uid)
        item.setEditable(False)
        color_item.setEditable(False)

    def add_set_item(self, set_item):
        item = QtGui.QStandardItem()
        item.setText(set_item.name)
        item.setData(set_item.uid)
        color_item = QtGui.QStandardItem()
        color_item.setBackground(
            QtGui.QBrush(QtGui.QColor(set_item.color), QtCore.Qt.SolidPattern)
        )

        if set_item.group_item:
            for elem in self.findItems(set_item.group_item.name):
                try:
                    GROUP_API.get_item(elem.data())
                    elem.appendRow([item, color_item])
                except ItemNotFoundException:
                    continue
        else:
            self.appendRow([item, color_item])
        item.setEditable(False)
        color_item.setEditable(False)

    def update_group_item(self, group_item_data): ...

    def update_set_item(self, standard_item, set_item):
        row = standard_item.row()
        if not standard_item.parent():
            self.update_row(self, set_item, row)
        else:
            self.update_row(standard_item.parent(), set_item, row)

    def update_row(self, parent, set_item, row):
        item, color_item = parent.takeRow(row)
        color_item.setBackground(
            QtGui.QBrush(QtGui.QColor(set_item.color), QtCore.Qt.SolidPattern)
        )
        parent.insertRow(row, [item, color_item])

    def remove_item(self, standard_item):
        if standard_item.parent():
            standard_item.parent().takeRow(standard_item.row())
        else:
            self.takeRow(standard_item.row())
