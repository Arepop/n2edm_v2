from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5 import QtWidgets


class ItemLookup(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.widgets = {}
        for elem in [
            "group",
            "action",
            "start",
            "stop",
            "SCPI-I",
            "SCPI-F",
            "duration",
            "params",
        ]:
            label = QtWidgets.QLabel(f"{elem.capitalize()}:")
            label.setFixedWidth(60)
            text = QtWidgets.QLineEdit()
            text.setEnabled(False)
            self.widgets[elem] = {"layout": QtWidgets.QHBoxLayout(), "label": label, "text": text}
            self.widgets[elem]["layout"].addWidget(label)
            self.widgets[elem]["layout"].addWidget(text)
            self.layout.addLayout(self.widgets[elem]["layout"])
        self.setLayout(self.layout)
