from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal

from ....widgets.views import ActionsView, TreeView, SearchBarView
from ....core.objects import GroupObject, ActionObject, Object
from ....widgets.dialogs import ActionDialog, GroupDialog
from ....core.handlers import ActionHandler, GroupHandler


class Actions(ActionsView):
    """QWidget connecting TreeView ant Searchbar for it

    Args:
        parent (QWigdet): Parent widget
    """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.create_view()

    def create_view(self) -> None:
        """Creates layout and widgets (Tree and Bar)
        """
        self.search_bar = SearchBar(self)
        self.tree = Tree(self)
        self.search_bar.search_sig.connect(self.tree.search)
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.tree)

class Tree(TreeView):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.create_view()
        self.action_handler = ActionHandler()
        self.group_handler = GroupHandler()

    def create_view(self):
        self.model = StandardItemModel(self)
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setRecursiveFilteringEnabled(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setModel(self.proxy_model)
        self.setDragDropMode(self.DragOnly)
        self.setSelectionMode(self.SingleSelection)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def open_action_creation_dialog(self):
        self.action_dialog = ActionDialog(self)
        self.action_dialog.SIG_create_action.connect(self.create_action)
        self.action_dialog.group_combo_box.activated.connect(lambda: self.open_group_creation_dialog(self.action_dialog))
        self.action_dialog.exec()

    def open_group_creation_dialog(self, action_dialog):
        if self.action_dialog.group_combo_box.currentText() == "Create...":
            group_dialog = GroupDialog(self)
            group_dialog.SIG_create_group.connect(self.create_group)
            group_dialog.exec()

    def create_action(self, attributes):
        try:
            action = ActionObject.create(self.action_handler, **attributes)
            self.model.populate()
        except NameError:
            print("Window with error name exist")
    
    def create_group(self, attributes):
        try:
            group = GroupObject.create(self.group_handler, **attributes)
            self.action_dialog.group_combo_box.clear()
            self.action_dialog.fill_group_combo_box()
            self.action_dialog.group_combo_box.addItem(group.name, group)
        except NameError:
            print("Window with error name exist")

    def update_entry(self, obj, attributes):
        Object.update(obj, **attributes)

    def delete_entry(self):
        """Remove selected group or action from tree
        """
        item = self.currentIndex().data(role=257)
        item.delete(item)
        self.model.populate()

    def search(self, search_str: str) -> None:
        """Searches item in tree view by given name

        Args:
            search_str (str): Name of signal to seach
        """
        self.proxy_model.setFilterRegExp(search_str)

    def contextMenuEvent(self, event: QtCore.QEvent) -> None:
        """Context menu controller and looks for action tree.pardir

        Args:
            event (QtCore.QEvent): QContextEvent
        """
        self.menu = QtWidgets.QMenu(self)
        add_action = QtWidgets.QAction("Add Action...", self)
        edit_action = QtWidgets.QAction("Edit...", self)
        del_action = QtWidgets.QAction("Delete...", self)
        add_action.triggered.connect(self.open_action_creation_dialog)
        edit_action.triggered.connect(self.update_entry)
        del_action.triggered.connect(self.delete_entry)
        self.menu.addAction(add_action)
        self.menu.addAction(edit_action)
        self.menu.addAction(del_action)
        self.menu.popup(QtGui.QCursor.pos())


class SearchBar(SearchBarView):
    search_sig = Signal(str)
    def __init__(self, parent):
        super().__init__(parent=parent)

    def keyPressEvent(self, event: QtCore.QEvent) -> None:
        """Send string as signal to tree_view to search signals in tree_view

        Args:
            event (QEvent): Pressed key event
        """
        super().keyPressEvent(event)
        if event.key():
            self.search_sig.emit(self.text())


class StandardItemModel(QtGui.QStandardItemModel):
    """Model of items and data to hold by widget

    Args:
        parent (QWidget): parent widget

    Attributes:
        self.actions (dict): dictionary with actions
        self.groups (dict): dictionary with groups

    """
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(QtGui.QStandardItemModel, self).__init__()
        self.setColumnCount(3)
        self.parent = parent

    def populate(self) -> tuple:
        """Fills tree with actions based on dictionary. Also creates groups etc...

        Args:
            dictionary (dict): dictionary with actions

        Returns:
            tuple: pair of dictioraries of actions and groups
        """
        self.clear()
        for group in GroupObject.all():
            if group.state == "to_delete":
                continue
            else:
                item = QtGui.QStandardItem()
                item.setText(group.name)
                item.setData(group)
                color_item = QtGui.QStandardItem()
                color_item.setBackground(QtGui.QBrush(
                    QtGui.QColor('#ffffff'), QtCore.Qt.SolidPattern))
                self.appendRow([item, color_item])

        for action in ActionObject.all():
            if action.state == "to_delete":
                continue
            if action.group:
                pass
            else:
                item = QtGui.QStandardItem()
                item.setText(action.name)
                item.setData(action)
                color_item = QtGui.QStandardItem()
                color_item.setBackground(QtGui.QBrush(
                    QtGui.QColor(action.color), QtCore.Qt.SolidPattern))
                self.appendRow([item, color_item])