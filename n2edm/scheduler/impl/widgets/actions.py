from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal as Signal

from ....widgets.views import ActionsView, TreeView, SearchBarView
from ....core.objects import GroupObject, ActionObject, TimelineObject, InfinitActorObject
from ....widgets.dialogs import ActionDialog
from ....core.handlers import ActionHandler


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

    def search(self, search_str: str) -> None:
        """Searches item in tree view by given name

        Args:
            search_str (str): Name of signal to seach
        """
        self.proxy_model.setFilterRegExp(search_str)

    def open_action_creation_dialog(self):
        action_dialog = ActionDialog(self)
        action_dialog.SIG_create_action.connect(self.create_action)
        action_dialog.exec()

    def create_action(self, attributes):
        action = ActionObject.create(**attributes)
        obj = next(action)
        try:
            can_create = self.action_handler.check_unique(obj)
        except NameError:
            can_create = False
        next(action)
        obj = action.send(can_create)
        self.model.populate()

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
        for action in ActionObject.all():
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