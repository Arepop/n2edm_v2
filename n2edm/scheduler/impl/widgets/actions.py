from PyQt5 import QtCore, QtGui, QtWidgets

from ....widgets.views import ActionsView, TreeView, SearchBarView


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
        main_layout = QtWidgets.QVBoxLayout(self)
        self.search_bar = SearchBarView(self)
        self.tree = ActionTreeView(self)
        self.search_bar.search_sig.connect(self.tree.search)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.tree)

class Tree(TreeView):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.create_view()

    def create_view(self):
        pass

class StandardItemModel(QtGui.QStandardItemModel):
    """Model of items and data to hold by widget

    Args:
        parent (QWidget): parent widget

    Attributes:
        self.actions (dict): dictionary with actions
        self.groups (dict): dictionary with groups

    """

    update_actions_sig = QtCore.pyqtSignal(list)

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(QtGui.QStandardItemModel, self).__init__()
        self.setColumnCount(3)
        self.parent = parent

    def populate(self, dictionary: dict) -> tuple:
        """Fills tree with actions based on dictionary. Also creates groups etc...

        Args:
            dictionary (dict): dictionary with actions

        Returns:
            tuple: pair of dictioraries of actions and groups
        """
        